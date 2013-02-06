(function($) {
    $(document).ready(function($) {

        $("#id_content_raw").keyup(function() {
            $('a[title="Preview"]').trigger('mousedown');
        });

        mySettings.markupSet.push({
            name: 'Media Window',
            key: 'W',
            className:"MediaWindow",
            replaceWith: function(markItUp) {
                return MediaBrowserPopUp(markItUp);
            },
        });

        $("#{{ id }}").markItUp(mySettings);
        $('a[title="Preview"]').trigger('mouseup');

    });
})(jQuery);

MediaBrowserPopUp = function(markItUp) {
    
}