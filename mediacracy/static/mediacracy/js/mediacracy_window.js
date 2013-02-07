
(function($) { 
    $.mediacracy_window = {
        init: function(selector) {
              this.id_map = Object();
              $( selector ).tabs({
                  beforeLoad: function( event, ui ) {
                      $.mediacracy_window.beforeLoadFunc(event, ui);
                  },
                  load: function(event, ui) {
                      $.mediacracy_window.loadFunc(event, ui);
                  },
                  cache: true
              });
        },
        beforeLoadFunc: function( event, ui ) {
            // build a map to know what URL to use
            var new_id = $(ui.tab).attr('aria-controls');
            var href = $(ui.tab).children('a')[0].href;
            $.mediacracy_window.id_map[new_id] = href;
        },
        loadFunc: function(event, ui) {
            //change the onclick handler to insert into editor
            items = $('#'+$(ui.panel).attr('id')+' a[onclick^="opener.dismissRelated"]');
            items.removeAttr('onclick');
            items.delegate('','click', function(event) {
                item_type = $.mediacracy_window.id_map[$(ui.panel).attr('id')].split('type=')[1];
                item_id = $(this).attr('href').split('/')[0];
                opener.mediacracy_window_callback(window,item_type,item_id);
                event.preventDefault();
            } );
            //over write links that go into change_list
            $('#'+$(ui.panel).attr('id')+' a').delegate('','click', function(event) {
                var split_href = this.href.split('?');
                var new_href = $.mediacracy_window.id_map[$(ui.panel).attr('id')]+'&'+split_href[1];
                $(ui.panel).load(new_href, 
                    function() {
                        $.mediacracy_window.loadFunc('',ui);
                    }
                );
                event.preventDefault();
            });
        },

    };

 })(jQuery);

(function($) { 
    $(document).ready(function($) {
        $.mediacracy_window.init("#tabs");
    });
})(jQuery);