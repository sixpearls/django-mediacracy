{% load url from future %}

(function($) {
    $(document).ready(function($) {

        var preview_delayed = false;

        function update_preview_delay() {
            preview_delayed = false;
        }

        $("#id_content_raw").keyup(function() {
            if (!preview_delayed) {
                window.setTimeout(update_preview_delay,1000);
                preview_delayed = true;
                $('a[title="Preview"]').trigger('mousedown');
            }
        });

        mySettings.markupSet.push({
            name: 'Mediacracy',
            key: 'M',
            className:"MediaWindow",
            replaceWith: function(markItUp) {
                return MediacracyPopUp(markItUp);
            },
        }, {
            name: 'Save',
            key: 'S',
            className:"Save",
            replaceWith: function(markItUp) {
                return MediacracySave(markItUp);
            },
        });

        $("#{{ id }}").markItUp(mySettings);
        $('a[title="Preview"]').trigger('mousedown');

    });
})(jQuery);

ForceSaveContinue = function() {
    $("input[name='_continue']").click();
}

MediacracySave = function(markItUp) {
    var the_form = $("form");

    //check if this a new object OR if there are errors already here. If so, force normal save. Otherwise, use ajax.
    if ($(window.location.pathname.split('/')).get(-2) == 'add' || $('ul.errorlist').length>0) {
        ForceSaveContinue();
    }

    $.ajax({ // create an AJAX call...
        data: the_form.serialize()+"&_continue=", // get the form data, send as "save and continue"
        type: the_form.attr('method'), // GET or POST
        url: the_form.attr('action'), // the file to call
        success: function(response) { // on 400 response..
            var success_message = $(response).find('ul.messagelist');
            if (success_message.length > 0) { //success message. Perhaps this should be made more explicit?
                $('ul.messagelist').remove();
                success_message.insertBefore($('#content')).delay(1000).toggle(function() {
                    success_message.remove();
                });
            } else { // did not get success message
                ForceSaveContinue();
            }
        },
        error: function(response) { // on non 400 responses
            ForceSaveContinue();
        }
    });
}

/*
<ul class="messagelist">
  <li class="info">The Textify Page &quot;/medical/treatments/laser/ -- LASER&quot; was changed successfully. You may edit it again below.</li>
</ul>
*/

MediacracyPopUp = function(markItUp) {
    var url = '{% url 'mediacracy_window' %}';
    var windowName = "Mediacracy";
    var windowSize = "width=820,height=500";

    window.open(url, windowName, windowSize);
}

mediacracy_window_callback = function(target, type, id) {
    target.close();
    var result = '{% templatetag openblock %} show_media "' + type + '" ' + id;
    if (type=='image') {
        result = result + ' file_size="thumbnail|small|medium|large|file" fig_class="left|right"'
    }
    result = result + ' {% templatetag closeblock %}'
    $.markItUp({ replaceWith: result });
}