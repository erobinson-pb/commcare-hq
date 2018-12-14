hqDefine("users/js/mobile_workers", function () {
    var mobileWorker = function (options) {
        var self = ko.mapping.fromJS(options);

        self.action_error = ko.observable('');

        self.editUrl = ko.computed(function () {
            return hqImport("hqwebapp/js/initial_page_data").reverse('edit_commcare_user', self.user_id());
        });

        self.is_active.subscribe(function (newValue) {
            var urlName = newValue ? 'activate_commcare_user' : 'deactivate_commcare_user',
                $modal = $('#' + (newValue ? 'activate_' : 'deactivate_') + self.user_id());

            $modal.find(".btn").addSpinnerToButton();
            $.ajax({
                method: 'POST',
                url: hqImport("hqwebapp/js/initial_page_data").reverse(urlName, self.user_id()),
                success: function (data) {
                    $modal.modal('hide');
                    if (data.success) {
                        self.action_error('');
                    } else {
                        self.action_error(data.error);
                    }
                },
                error: function () {
                    $modal.modal('hide');
                    self.action_error(gettext("Issue communicating with server. Try again."));
                },
            });
        });

        return self;
    };

    var mobileWorkersList = function () {
        var self = {};
        self.users = ko.observableArray([]);

        self.query = ko.observable('');
        self.deactivatedOnly = ko.observable(false);

        self.itemsPerPage = ko.observable(5);
        self.totalItems = ko.observable();

        // Visibility of spinner, messages, and user table
        self.hasError = ko.observable(false);
        self.isLoaded = ko.observable(false);
        self.projectHasUsers = ko.observable(true);

        self.showProjectHasNoUsers = ko.computed(function () {
            return self.isLoaded() && !self.hasError() && !self.projectHasUsers();
        });

        self.showNoUsers = ko.computed(function () {
            return self.isLoaded() && !self.hasError() && !self.totalItems() && !self.showProjectHasNoUsers();
        });

        self.showSpinner = ko.computed(function () {
            return !self.isLoaded() && !self.hasError();
        });

        self.showTable = ko.computed(function () {
            return self.isLoaded() && !self.hasError() && !self.showNoUsers() && !self.showProjectHasNoUsers();
        });

        self.deactivatedOnly.subscribe(function () {
            self.goToPage(1);
        });

        self.goToPage = function (page) {
            self.users.removeAll();
            self.hasError(false);
            self.isLoaded(false);
            $.ajax({
                method: 'GET',
                url: hqImport("hqwebapp/js/initial_page_data").reverse('paginate_mobile_workers'),
                data: {
                    page: page || 1,
                    query: self.query(),
                    limit: self.itemsPerPage(),
                    showDeactivatedUsers: self.deactivatedOnly(),
                },
                success: function (data) {
                    self.totalItems(data.total);
                    self.users(_.map(data.users, function (user) {
                        return mobileWorker(user);
                    }));

                    if (!self.query()) {
                        self.projectHasUsers(!!data.users.length);
                    }
                    self.isLoaded(true);
                    self.hasError(false);
                },
                error: function () {
                    self.isLoaded(true);
                    self.hasError(true);
                },
            });
        };
        self.goToPage(1);
        return self;
    };

    $(function () {
        $("#mobile-workers-list").koApplyBindings(mobileWorkersList());
    });
});
