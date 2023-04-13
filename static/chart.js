$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "/chart",
        success: function(data) {
            // Use the data to create your chart
            console.log(data);

            let ctx = document.getElementById('gw2-chart').getContext('2d');
            let myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data['labels'],
                    datasets: [{
                        label: 'Average Buys',
                        data: data['buy_data']['data'],
                        borderColor: 'purple',
                        fill: false
                    },
                    {
                        label: 'Average Sells',
                        data: data['sell_data']['data'],
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
        },
        error: function(xhr, status, error) {
            console.log(error);
        }
    });
})