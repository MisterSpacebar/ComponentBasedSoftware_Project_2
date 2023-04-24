$(document).ready(function() {
    // Get all of the radio buttons in the form
    var radioButtons = $('input[type="radio"]');
  
    // When a radio button is clicked, set the `checked` attribute
    radioButtons.on('click', function() {
      $(this).closest('.btn-group').find('.active').removeClass('active');
      $(this).addClass('active');
    });
});