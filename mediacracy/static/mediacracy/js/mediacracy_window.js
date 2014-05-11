
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
                split_href = $(this).attr('href').split('/');
                item_id = split_href[split_href.length-2];
                opener.mediacracy_window_callback(window,item_type,item_id);
                event.preventDefault();
            } );
            //over write links that go into change_list
            $('#'+$(ui.panel).attr('id')+' a').filter('[class!="addlink"]').delegate('','click', function(event) {
                var split_href = this.href.split('?');
                var new_href = $.mediacracy_window.id_map[$(ui.panel).attr('id')]+'&'+split_href[1];
                $(ui.panel).load(new_href, 
                    function() {
                        $.mediacracy_window.loadFunc('',ui);
                    }
                );
                event.preventDefault();
            });
            //over write change_form 
            $('#'+$(ui.panel).attr('id')+' a.addlink').delegate('','click', function(event) {
                //stuff
                var change_form_url = this.href;
                var form_panel = ui.panel;
                $(ui.panel).load(change_form_url,
                  function(response, status, xhr) {
                      var form = $(this).find("form");
                      form.submit(function(event) {
                        //$(form.panel).load(form.attr('action'),form.serializeArray());
                        $.ajax({ // create an AJAX call...
                            data: $(this).serialize(), // get the form data
                            type: $(this).attr('method'), // GET or POST
                            url: change_form_url, // the file to call
                            success: function(response) { // on success..
                                $(form_panel).load($.mediacracy_window.id_map[$(form_panel).attr('id')],
                                    function() {
                                        $.mediacracy_window.loadFunc('',ui);
                                    }
                                ); // update the DIV
                            }
                        });
                        event.preventDefault();
                      });
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