const data = JSON.parse(document.getElementById('data').textContent);
const data_labels = data.labels;
const data_values = data.values;

console.log(data)

const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data_labels,
        datasets: [{
            fill: {
                target: 'origin',
                above: 'rgb(181, 141, 226, 0.5)',
            },
            label: "Valor da ação",
            data: data_values,
            backgroundColor: 'rgb(0, 0, 0)',
            borderColor: 'rgb(155, 96, 222)',
            borderWidth: 1,
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepSize: 100000,
                    min: 0
                }
            }]
            
        },
        animations: {
            tension: {
              duration: 1000,
              easing: 'linear',
              from: 1,
              to: 0.5,
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Valor das cotações'
            }
        },
        
    }
});