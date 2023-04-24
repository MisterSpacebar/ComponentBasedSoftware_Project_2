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
                        borderColor: 'red',
                        fill: false,
                    },
                    {
                        label: "Average Completed Sell Listing",
                        data: data['average_sells'],
                        borderColor: 'darkgrey',
                        fill: false,
                    }]
                },
                options: {
                    tooltips: {
                      enabled: true,
                      trigger: 'mousemove',
                      custom: function(tooltipItem, data) {
                        // Get the mouse position
                        var mouseX = tooltipItem.clientX;
              
                        // Get the x-axis coordinate
                        var xCoordinate = myChart.scales['x-axis-0'].getPixelForValue(mouseX);
              
                        // Get the y-coordinate values for both lines
                        var yCoordinate1 = myChart.scales['y-axis-0'].getValueForPixel(xCoordinate);
                        var yCoordinate2 = myChart.scales['y-axis-1'].getValueForPixel(xCoordinate);
              
                        // Display the y-coordinate values in a tooltip
                        tooltipItem.body = `X: ${xCoordinate}<br>Y1: ${yCoordinate1}<br>Y2: ${yCoordinate2}`;
                      },
                    },
                  },
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

            function updateHover(chart, event) {
                var activePoints = chart.getElementsAtEventForMode(event, 'nearest', { intersect: true }, true);
                var firstPoint = activePoints[0];
                if (firstPoint) {
                  var datasetIndex = firstPoint._datasetIndex;
                  var index = firstPoint._index;
                  chart.updateHoverStyle(activePoints, null, true);
                  chart.tooltip._active = [activePoints[0]];
                  chart.tooltip.update(true);
                } else {
                  chart.updateHoverStyle(activePoints, null, true);
                  chart.tooltip._active = [];
                  chart.tooltip.update(true);
                }
              }

            let canvas = document.getElementById('gw2-chart');
            canvas.addEventListener('mousemove', function(event) {
                updateHover(myChart,event);
            });

        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
});

