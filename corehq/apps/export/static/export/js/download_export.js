hqDefine('export/js/download_export', function () {
    'use strict';

    /*var initial_page_data = hqImport('hqwebapp/js/initial_page_data').get;
    var downloadExportsApp = window.angular.module('downloadExportsApp', ['hq.download_export']);
    downloadExportsApp.config(["djangoRMIProvider", function (djangoRMIProvider) {
        djangoRMIProvider.configure(initial_page_data('djng_current_rmi'));
    }]);
    downloadExportsApp.constant('exportList', initial_page_data('export_list'));
    downloadExportsApp.constant('formElement', {
        progress: function () {
            return $('#download-progress-bar');
        },
        group: function () {
            return $('#id_group');
        },
        user_type: function () {
            return $('#id_user_types');
        },
    });*/

    // Model for the form to select date range, users, etc.
    var downloadFormModel = function (options) {
        hqImport("hqwebapp/js/assert_properties").assert(options, [
            'defaultDateRange',
            'exportList',
            'exportType',
            'formOrCase',
            'maxColumnSize',
            'multimediaUrl',    // present if we should check for multimedia
            'progressModel',
            'prepareUrl',
            'prepareMultimediaUrl',
            'smsExport',
            'userTypes',
        ]);

        var self = _.extend({}, options);
        self.filterName = self.exportType === "form" ? "emw" : "case_list_filter";

        // Form data
        self.dateRange = ko.observable(self.defaultDateRange);
        self.emw = ko.observable();

        // UI flags
        self.preparingExport = ko.observable(false);
        self.prepareExportError = ko.observable('');
        self.preparingMultimediaExport = ko.observable(false);
        self.hasMultimedia = ko.observable(false);

        // Once the download starts, this (downloadFormModel) disables the form and displays a message.
        // When the download is complete, the downloadProgressModel gives the user the option to clear
        // filters and do another download. Listen for that signal.
        self.downloadInProgress = ko.observable(false);
        self.progressModel.showDownloadStatus.subscribe(function (newValue) {
            self.downloadInProgress(newValue);
        });

        self.defaultPrepareExportError = ko.computed(function () {
            return self.prepareExportError() === 'default';
        });

        self.isValid = ko.computed(function () {
            return !!self.dateRange();
        });

        self.disablePrepareExport = ko.computed(function () {
            return !self.isValid() || self.preparingExport();
        });
        self.disablePrepareMultimediaExport = ko.computed(function () {
            return !self.isValid() || self.preparingMultimediaExport();
        });

        self.sendAnalytics = function () {
            _.each(self.userTypes, function (user_type) {
                hqImport('analytix/js/google').track.event("Download Export", 'Select "user type"', user_type); // TODO: test
            });
            var action = (self.exportList.length > 1) ? "Bulk" : "Regular";
            hqImport('analytix/js/google').track.event("Download Export", self.exportType, action);
            _.each(self.exportList, function (export_) {
                if (export_.has_case_history_table) {
                    hqImport('analytix/js/google').track.event("Download Case History Export", export_.domain, export_.export_id);
                }
            });
        };

        self.prepareExport = function () {
            self.emw(hqImport('reports/js/reports.util').urlSerialize($('form[name="exportFiltersForm"]')));
            self.prepareExportError('');
            self.preparingExport(true);

            var filterNamesAsString = $("form[name='exportFiltersForm']").find("input[name=" + self.filterName + "]").val();

            function getFilterNames() {
                return (filterNamesAsString ? filterNamesAsString.split(',') : []);
            }

            hqImport('analytix/js/kissmetrix').track.event("Clicked Prepare Export", {
                "Export type": self.exportList[0].export_type,
                "filters": _.map(
                    getFilterNames(),
                    function (item) {
                        var prefix = "t__";
                        if (item.substring(0, prefix.length) === prefix) {
                            return self.userTypes[item.substring(prefix.length)];
                        }
                        return item;
                    }
                ).join()});

            $.ajax({
                method: 'POST',
                url: self.prepareUrl,
                data: {
                    form_or_case: self.formOrCase,
                    sms_export: self.smsExport,
                    exports: JSON.stringify(self.exportList),
                    max_column_size: self.maxColumnSize,
                    form_data: JSON.stringify({
                        date_range: self.dateRange(),
                        emw: self.emw(),
                    }),
                },
                success: function (data) {
                    if (data.success) {
                        self.sendAnalytics();
                        self.preparingExport(false);
                        self.downloadInProgress(true);
                        self.progressModel.startDownload(data.download_id);
                    } else {
                        self._handlePrepareError(data);
                    }
                },
                error: self._handlePrepareError,
            });
        };

        if (self.multimediaUrl) {
            $.ajax({
                method: 'GET',
                url: self.multimediaUrl,
                data: {
                    export_id: self.exportList[0].export_id,
                    form_or_case: self.formOrCase,
                },
                success: function (data) {
                    if (data.success) {
                        self.hasMultimedia(data.hasMultimedia);
                    }
                },
            });
        }

        self.prepareMultimediaExport = function () {
            self.prepareExportError('');
            self.preparingMultimediaExport(true);
            $.ajax({
                method: 'POST',
                url: self.prepareMultimediaUrl,
                data: {
                    form_or_case: self.formOrCase,
                    sms_export: self.smsExport,
                    exports: JSON.stringify(self.exportList),
                    form_data: JSON.stringify({
                        date_range: self.dateRange(),
                        emw: self.emw(),
                    }),
                },
                success: function (data) {
                    if (data.success) {
                        self.sendAnalytics();
                        self.preparingMultimediaExport(false);
                        self.downloadInProgress(true);
                        self.progressModel.startMultimediaDownload(data.download_id);
                    } else {
                        self._handlePrepareError(data);
                    }
                },
                error: self._handlePrepareError,
            });
        };

        self._handlePrepareError = function (data) {
            if (data && data.error) {
                // The server returned an error message.
                self.prepareExportError(data.error);
            } else {
                self.prepareExportError("default");
            }
            self.preparingExport(false);
            self.preparingMultimediaExport(false);
        };

        return self;
    };

    // Model for showing progress, etc once the download has been generated
    var downloadProgressModel = function (options) {
        hqImport("hqwebapp/js/assert_properties").assert(options, ['exportType', 'formOrCase', 'emailUrl', 'pollUrl']);

        var self = {};

        self.exportType = options.exportType;
        self.formOrCase = options.formOrCase;

        self.emailUrl = options.emailUrl;
        self.pollUrl = options.pollUrl;

        self.downloadId = ko.observable();
        self.showDownloadStatus = ko.observable();
        self.isDownloaded = ko.observable();
        self.isDownloadReady = ko.observable();
        self.isMultimediaDownload = ko.observable();
        self.progressError = ko.observable();
        self.progress = ko.observable();
        self.sendEmailFlag = ko.observable();

        self.celeryError = ko.observable('');
        self.downloadError = ko.observable('');
        self.showError = ko.computed(function () {
            return self.celeryError() || self.downloadError();
        });

        self.dropboxUrl = ko.observable();
        self.downloadUrl = ko.observable();

        self.resetDownload = function () {
            self.downloadId(null);
            self._numErrors = 0;
            self._numCeleryRetries = 0;
            self._lastProgress = 0;
            self.showDownloadStatus(false);
            self.isDownloadReady(false);
            self.isDownloaded(false);
            self.celeryError('');
            self.downloadError('');
            self.isMultimediaDownload(false);
            self.progress(0);
            self.progressError('');
            self.sendEmailFlag(false);
            self.dropboxUrl('');
            self.downloadUrl('');
        };
        self.resetDownload();

        self.startDownload = function (downloadId) {
            self.showDownloadStatus(true);
            self.downloadId(downloadId);
            self.interval = setInterval(self._checkDownloadProgress, 2000);
        };

        self.startMultimediaDownload = function (downloadId) {
            self.isMultimediaDownload(true);
            self.startDownload(downloadId);
        };

        self.clickDownload = function () {
            self.isDownloaded(true);
            self.sendAnalytics();
            return true;    // allow default click action
        };

        self.sendAnalytics = function () {
            hqImport('analytix/js/google').track.event("Download Export", hqImport('export/js/utils').capitalize(self.exportType), "Saved");
            hqImport('analytix/js/kissmetrix').track.event("Clicked Download button");
        };

        self._checkDownloadProgress = function () {
            $.ajax({
                method: 'GET',
                url: self.pollUrl,
                data: {
                    form_or_case: self.formOrCase,
                    download_id: self.downloadId,
                },
                success: function (data) {
                    if (data.is_poll_successful) {
                        self._updateProgressBar(data);
                        self.downloadId(data.download_id);
                        if (data.has_file && data.is_ready) {
                            clearInterval(self.interval);
                            return;
                        }
                        if (data.progress && data.progress.error) {
                            clearInterval(self.interval);
                            self.downloadError(data.progress.error);
                            return;
                        }
                        if (data.progress.current > self._lastProgress) {
                            self._lastProgress = data.progress.current;
                            // processing is still going, keep moving.
                            // this avoids failing hard prematurely at celery errors if
                            // the polling is still reporting forward progress.
                            self._numCeleryRetries = 0;
                            return;
                        }
                    }
                    if (data.error) {
                        self._dealWithErrors(data);
                    }
                    if (_.isNull(data.is_alive)) {
                        self._dealWithCeleryErrors();
                    }
                },
                error: self._dealWithErrors,
            });
        };

        self._dealWithCeleryErrors = function () {
            // Sometimes the task handler for celery is a little slow to get
            // started, so we have to try a few times.
            if (self._numCeleryRetries > 10) {
                clearInterval(self.interval);
                self.celeryError(gettext("Server maintenance in progress. Please try again later."));
            }
            self._numCeleryRetries ++;
        };

        self._dealWithErrors = function (data) {
            if (self._numErrors > 3) {
                if (data && data.error) {
                    self.downloadError(data.error);
                } else {
                    self.downloadError(gettext("There was an error downloading your export."));
                }
                clearInterval(self.interval);
            }
            self._numErrors ++;
        };

        self._updateProgressBar = function (data) {
            var progressPercent = 0;
            if (data.is_ready && data.has_file) {
                progressPercent = 100;
                self.isDownloadReady(true);
                self.dropboxUrl(data.dropbox_url);
                self.downloadUrl(data.download_url);
            } else if (_.isNumber(data.progress.percent)) {
                progressPercent = data.progress.percent;
            }
            self.progress(progressPercent);
        };

        self.sendEmailUponCompletion = function () {
            self.sendEmailFlag(true);
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: self.emailUrl,
                data: { download_id: self.downloadId },
            });
        };

        return self;
    };

    $(function () {
        hqImport("reports/js/filters/main").init();

        var initialPageData = hqImport("hqwebapp/js/initial_page_data"),
            exportList = initialPageData.get('export_list'),
            exportType = exportList[0].export_type;

        var progressModel = downloadProgressModel({
            exportType: exportType,
            emailUrl: initialPageData.reverse('add_export_email_request'),
            formOrCase: initialPageData.get('form_or_case'),
            pollUrl: initialPageData.reverse('poll_custom_export_download'),
        });

        var progressModel = downloadProgressModel({
            exportType: exportType,
            emailUrl: initialPageData.reverse('add_export_email_request'),
            formOrCase: initialPageData.get('form_or_case'),
            pollUrl: initialPageData.reverse('poll_custom_export_download'),
        });

        $("#download-export-form").koApplyBindings(downloadFormModel({
            defaultDateRange: initialPageData.get('default_date_range'),
            exportList: exportList,
            exportType: exportType,
            formOrCase: initialPageData.get('form_or_case'),
            maxColumnSize: initialPageData.get('max_column_size') || 2000,
            multimediaUrl: initialPageData.get('check_for_multimedia') ? initialPageData.reverse('has_multimedia') : '',
            progressModel: progressModel,
            prepareUrl: initialPageData.reverse('prepare_custom_export'),
            prepareMultimediaUrl: initialPageData.reverse('prepare_form_multimedia'),
            smsExport: initialPageData.get('sms_export'),
            userTypes: initialPageData.get('user_types'),
        }));

        $("#download-progress").koApplyBindings(progressModel);

        $(".hqwebapp-datespan").each(function () {
            var $el = $(this).find("input");
            $el.createDateRangePicker(
                $el.data("labels"),
                $el.data("separator"),
                $el.data('startDate'),
                $el.data('endDate')
            );
        });
    });
});
