$(document).ready(function() {
    // Set up the autocomplete search bar
    $('#search-bar').typeahead({
        source: function(query, process) {
            // Send an AJAX request to the Flask endpoint to get the autocomplete data
            $.ajax({
                url: '/autocomplete',
                method: 'POST',
                data: {'query': query},
                success: function(data) {
                    // Process the data and return it for the autocomplete search bar
                    var items = JSON.parse(data);
                    return process(items);
                }
            });
        }
    });
});