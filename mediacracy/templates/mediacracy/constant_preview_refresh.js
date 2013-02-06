(function($) { 
  $(document).ready(function($) {

    $("#id_content_raw").keyup(function(){
        $('a[title="Preview"]').trigger('mousedown');
    });

  });
})(jQuery);