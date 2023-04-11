$(document).ready(function() {
    console.log('Document ready!');
    // get autocomplete list
    let items = []
    $.ajax({
        url: '/autocomplete',
        method: 'POST',
        success: function(data) {
            // Store the autocomplete data in the `items` variable
            console.log(data);
            items = data;


            // Set up the autocomplete search bar
            $('#search-bar').typeahead({
                source: items
            });
            console.log('List ready!');
        }
    });

    // Handle form submission
    $('#search-form').submit(function(event) {
        event.preventDefault();
        var query = $('#search-bar').val();
        console.log('Searching for:', query);
        // Perform search with query...
    });
});