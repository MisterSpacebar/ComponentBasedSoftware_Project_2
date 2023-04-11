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

    $('#search-bar').on('keypress', function(event) {
        if (event.which === 13) {
            event.preventDefault();
            var query = $('#search-bar').text();
            console.log('Searching for:', query);
            // Perform search with query...

            // Send query to Flask endpoint
            $.ajax({
                url: '/search',
                method: 'POST',
                data: {
                    query: query
                },
                success: function(response) {
                    console.log('Response:', response);
                },
                error: function(xhr) {
                    console.error(xhr.responseText);
                }
            });
        }
    });
});