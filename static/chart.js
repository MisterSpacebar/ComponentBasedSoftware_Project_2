$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "/chart",
        success: function(data) {
            // Use the data to create a chart
            console.log(data);

            // Default chart template
            let ctx = document.getElementById('gw2-chart').getContext('2d');
            let myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data['date'],
                    datasets: [{
                        label: "Average Completed Buy Listing",
                        data: data['average_buys'],
                        borderColor: 'purple',
                        fill: false
                    },
                    {
                        label: "Average Completed Sell Listing",
                        data: data['average_sells'],
                        borderColor: 'teal',
                        fill: false
                    }]
                },
                options: {
                    responsive: true,
                    title: {
                        display: true,
                        text: 'Double Line Chart'
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });

            $('.chart-option').on('change', function() {
                // Retrieve the selected radio button's value and id
                var selectedId = $('.chart-option:checked').attr('id');
          
                // Log the selected valueto the console
                console.log('Selected ID: ' + selectedId);

                // makes changes to the graph object
                if(selectedId=='pricing') {
                    myChart.config.data.datasets[0].label = "Average Completed Buy Listing";
                    myChart.config.data.datasets[1].label = "Average Completed Sell Listing";
                    myChart.config.data.datasets[0].data = data['average_buys'];
                    myChart.config.data.datasets[1].data = data['average_sells'];
                } else if(selectedId=='quantities') {
                    myChart.config.data.datasets[0].label = "Quantity Listed For Purchase";
                    myChart.config.data.datasets[1].label = "Quantity Listed For Sale";
                    myChart.config.data.datasets[0].data = data['average_sell_quantities'];
                    console.log(data['average_buy_quantities']);
                    myChart.config.data.datasets[1].data = data['average_buy_quantities'];
                    console.log(data['average_sell_quantities'])
                }

                // update object
                myChart.update();
            });

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
})