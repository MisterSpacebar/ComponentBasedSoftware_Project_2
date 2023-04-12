$(document).ready(function(){
    $.ajax({
    type: "GET",
    url: "/chart-average",
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
                    data: data['datasets'][0]['data'],
                    borderColor: 'red',
                    fill: false
                },
                {
                    label: 'Average Sells',
                    data: data['datasets'][1]['data'],
                    borderColor: 'blue',
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