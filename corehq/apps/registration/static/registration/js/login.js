/* globals Blazy */
$(function () {
    // Blazy for loading images asynchronously
    // Usage: specify the b-lazy class on an element and adding the path
    // to the image in data-src="{% static 'path/to/image.jpg' %}"
    new Blazy({
        container: 'body',
    });
    
    var kissmetrics = hqImport('analytix/js/kissmetrix');
    kissmetrics.whenReadyAlways(function () {

        $('#cta-form-get-demo-button-body').click(function () {
            kissmetrics.track.event("Demo Workflow - Body Button Clicked");
        });

        $('#cta-form-get-demo-button-header').click(function () {
            kissmetrics.track.event("Demo Workflow - Header Button Clicked");
        });
    });
});
