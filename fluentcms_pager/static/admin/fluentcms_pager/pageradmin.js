!function($) {

  $.fn.ready(function(){
    $('#fluent_contents_inlines').on('change', '.inline-PagerItem input[name$=show_previous]', showUrlToggle);
    $('#fluent_contents_inlines').on('change', '.inline-PagerItem input[name$=show_next]', showUrlToggle);
    $('#fluent_contents_inlines .inline-PagerItem input[name$=show_previous]').each(showUrlToggle);
    $('#fluent_contents_inlines .inline-PagerItem input[name$=show_next]').each(showUrlToggle);
  });

  function showUrlToggle(event) {
    var $form_rows = $(this).closest('.form-row').siblings('.form-row');
    if(this.checked) {
      $form_rows.show();
    }
    else {
      $form_rows.hide();
    }
  }

}(window.jQuery || window.django.jQuery);
