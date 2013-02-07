(function($) {
    $(document).ready(function($) {

        $("#id_content_raw").keyup(function() {
            $('a[title="Preview"]').trigger('mousedown');
        });

        mySettings.markupSet.push({
            name: 'Mediacracy',
            key: 'M',
            className:"MediaWindow",
            replaceWith: function(markItUp) {
                return MediacracyPopUp(markItUp);
            },
        });

        $("#{{ id }}").markItUp(mySettings);
        $('a[title="Preview"]').trigger('mouseup');

    });
})(jQuery);

MediacracyPopUp = function(markItUp) {
    var url = '{% url mediacracy_window %}';
    var windowName = "Mediacracy";
    var windowSize = "width=820,height=500";

    window.open(url, windowName, windowSize);
}

mediacracy_window_callback = function(target, type, id) {
    target.close();
    $.markItUp({ replaceWith: '{% templatetag openblock %} show_media ' + type + ' ' + id + ' {% templatetag closeblock %}'});
}