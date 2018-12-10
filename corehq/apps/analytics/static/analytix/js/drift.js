/* global Array, window */

/**
 * Instantiates the Drift analytics and customer support messaging platform.
 */
hqDefine('analytix/js/drift', [
    'underscore',
    'analytix/js/initial',
    'analytix/js/logging',
    'analytix/js/utils',
    'analytix/js/hubspot',
], function (
    _,
    initialAnalytics,
    logging,
    utils,
    hubspot
) {
    'use strict';
    var _get = initialAnalytics.getFn('drift'),
        _drift = {},
        _logger = logging.getLoggerForApi('Drift'),
        _ready = $.Deferred(); // eslint-disable-line no-unused-vars

    $(function () {
        var apiId = _get('apiId'),
            scriptUrl = "https://js.driftt.com/include/" + utils.getDateHash() + "/" + apiId + '.js';

        _logger = logging.getLoggerForApi('Drift');
        _ready = utils.initApi(_ready, apiId, scriptUrl, _logger, function () {
            _drift = window.driftt = window.drift = window.driftt || [];
            if (!_drift.init && !_drift.invoked) {
                _drift.methods = [ "identify", "config", "track", "reset", "debug", "show", "ping", "page", "hide", "off", "on" ];
                _drift.factory = function (methodName) {
                    return function () {
                        var methodFn = Array.prototype.slice.call(arguments);
                        methodFn.unshift(methodName);
                        _drift.push(methodFn);
                        return _drift;
                    };
                };
                _.each(_drift.methods, function (methodName) {
                    _drift[methodName] = _drift.factory(methodName);
                });
            }

            _drift.SNIPPET_VERSION = '0.3.1';

            _drift.on('emailCapture',function (e) {
                hubspot.identify({email: e.data.email});
                hubspot.trackEvent('Identified via Drift');
            });

            $('.schedule-demo-drift-cta').click(function (e) {
                e.preventDefault();

                var kissmetrics = hqImport('analytix/js/kissmetrix');

                _drift.on('startConversation', function () {
                    kissmetrics.track.event("Demo Workflow - Viewed Form");
                });

                _drift.on("emailCapture", function () {
                    kissmetrics.track.event("Demo Workflow - Contact Info Received");
                    kissmetrics.track.event("Demo Workflow - Loaded Booking Options");
                });

                _drift.on("sliderMessage:close", function () {
                    kissmetrics.track.event("Demo Workflow - Dismissed Form");
                    _drift.off("sliderMessage:close");
                });

                _drift.on("scheduling:meetingBooked", function () {
                    kissmetrics.track.event("Demo Workflow - Demo Scheduled");
                    _drift.off("sliderMessage:close");
                });

                _drift.on("message:sent", function () {
                    kissmetrics.track.event("Demo Workflow - Interacted With Form");
                    _drift.off("message:sent");
                });

                _drift.api.startInteraction({
                    interactionId: 43079,
                    goToConversation: true,
                });
            });

        });
    });

    // no methods just yet
    return 1;
});
