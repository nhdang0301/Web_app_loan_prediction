document.addEventListener('DOMContentLoaded', function() {
  var dashboard = document.getElementById('dashboard');
  var products = document.getElementById('products');

  function initializeDashboardCharts() {
    if (dashboard.classList.contains('active')) {
      fetch('/total-data')  // Fetch financial data from Flask API
        .then(response => response.json())
        .then(data => {
          // Initialize the first bar chart with fetched data
          var ctxBar = document.getElementById("myChart").getContext("2d");
          var myChart = new Chart(ctxBar, {
            type: "bar",
            data: {
              labels: data.labels,  // ["Total Funded Amount", "Total Expected Loss"]
              datasets: [{
                label: "Total Values",
                data: data.totals,
                backgroundColor: [
                  "rgba(54, 162, 235, 0.6)",
                  "rgba(255, 99, 132, 0.6)"
                ],
                borderColor: [
                  "rgba(54, 162, 235, 1)",
                  "rgba(255, 99, 132, 1)"
                ],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                yAxes: [{
                  ticks: {
                    beginAtZero: true
                  }
                }]
              }
            }
          });
        });
      
      // Fetch term data from Flask API
      fetch('/term-data')
        .then(response => response.json())
        .then(data => {
          // Initialize the pie chart with fetched data
          var ctxPie = document.getElementById("termPieChart").getContext("2d");
          var termPieChart = new Chart(ctxPie, {
            type: "pie",
            data: {
              labels: data.labels,  // ["Short Term", "Medium Term", "Long Term"]
              datasets: [{
                label: "Term Distribution",
                data: data.values,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.6)",
                  "rgba(54, 162, 235, 0.6)",
                  "rgba(75, 192, 192, 0.6)"
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(75, 192, 192, 1)"
                ],
                borderWidth: 1
              }]
            },
            options: {
                responsive: false,
           }
          });
        });
    }
  }
  

  function initializeProductsCharts() {
    if (products.classList.contains('active')) {
      fetch('/annual-dti-histogram')
        .then(response => response.json())
        .then(data => {
          console.log(data);
          const roundedLabels = data.labels.map(label => parseFloat(label).toFixed(2));

          // Initialize the histogram chart with fetched data
          var ctxHistogram = document.getElementById("histogramChart").getContext("2d");
          var histogramChart = new Chart(ctxHistogram, {
            type: "bar",  // Set the default chart type to bar
            data: {
              labels: roundedLabels,
              datasets: [{
                label: "DTI Distribution",
                type: "bar",  // Specify chart type for this dataset explicitly
                data: data.values,
                backgroundColor: "rgba(75, 192, 192, 0.6)",
                borderColor: "rgba(75, 192, 192, 1)",
                borderWidth: 1
              }, {
                label: "Trend Line",
                type: "line",  // Specify chart type for this dataset as line
                data: data.values,  // Assume you want to use the same data for the line
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 2,
                fill: false
              }]
            },
            options: {
              scales: {
                yAxes: [{
                  ticks: {
                    stepSize: 1,
                    beginAtZero: true
                  }
                }],
                xAxes: [{  // Adding configuration for the x-axis
                  ticks: {
                    callback: function(value, index, values) {
                      // Check if value can be converted to a float
                      if (!isNaN(parseFloat(value))) {
                        return parseFloat(value).toFixed(2); // Rounds the value to 2 decimal places
                      }
                      return value; // Return the original value if it's not a number
                    }
                  }
                }]
              }
            }
          });
        });
      fetch('/loan-data')
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Initialize the pie chart with fetched data
          var ctxPie = document.getElementById("loanPieChart").getContext("2d");
          var loanPieChart = new Chart(ctxPie, {
            type: "pie",
            data: {
              labels: data.labels,  // ["Short Term", "Medium Term", "Long Term"]
              datasets: [{
                label: "Loan Status Distribution",
                data: data.values,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.6)",
                  "rgba(54, 162, 235, 0.6)",
                  "rgba(75, 192, 192, 0.6)"
                ],
                borderColor: [
                  "rgba(255, 99, 132, 1)",
                  "rgba(54, 162, 235, 1)",
                  "rgba(75, 192, 192, 1)"
                ],
                borderWidth: 1
              }]
            },
            options: {
                responsive: false,
           }
          });
        });    
        fetch('/loan-purpose-data')
        .then(response => response.json())
        .then(data => {
          console.log(data);
            var ctx = document.getElementById('polarAreaChart').getContext('2d');
            var polarAreaChart = new Chart(ctx, {
                type: 'polarArea',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Loan Purposes',
                        data: data.data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        r: {
                            beginAtZero: true
                        }
                    },
                    responsive: true,
                }
            });
        })
        .catch(error => console.error('Error loading the polar area chart data:', error));     

        var ctx = document.getElementById('verticalbarChart').getContext('2d');
        var verticalbarChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'], // X-axis labels
                datasets: [{
                    label: 'Total Funded Amount', // Legend
                    data: [65, 59, -80, 81, 56, 55, 40], // Y-values for dataset 1
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', // Color for bars
                    borderColor: 'rgba(255, 99, 132, 1)', // Border color for bars
                    borderWidth: 1
                }, {
                    label: 'Total Expected Loss', // Legend
                    data: [-28, 48, -40, 19, 86, 27, 90], // Y-values for dataset 2
                    backgroundColor: 'rgba(54, 162, 235, 0.2)', // Color for bars
                    borderColor: 'rgba(54, 162, 235, 1)', // Border color for bars
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            // Include a dollar sign in the ticks and allow negative values
                            callback: function(value, index, values) {
                                return value.toLocaleString("en-US", {style:"currency", currency:"USD"});
                            }
                        }
                    }
                },
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return tooltipItem.dataset.label + ': ' + tooltipItem.raw.toLocaleString("en-US", {style:"currency", currency:"USD"});
                            }
                        }
                    }
                }
            }
        });   
    }
  }

  function handleSidebarClick(target) {
    if (target === 'dashboard') {
      dashboard.classList.add('active');
      products.classList.remove('active');
      initializeDashboardCharts();
    } else if (target === 'products') {
      products.classList.add('active');
      dashboard.classList.remove('active');
      initializeProductsCharts();
    }
  }

  document.querySelectorAll('.sidebar-list-item').forEach(function(item) {
    item.addEventListener('click', function() {
      var target = item.getAttribute('data-target');
      handleSidebarClick(target);
    });
  });

  // Initialize charts on page load if applicable
  if (dashboard.classList.contains('active')) {
    initializeDashboardCharts();
  }
  if (products.classList.contains('active')) {
    initializeProductsCharts();
  }
});
