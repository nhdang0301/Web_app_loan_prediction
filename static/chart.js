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
      // Sample data for products scatter chart
      var sampleScatterData = [
        {x: 1, y: 2},
        {x: 2, y: 3},
        {x: 3, y: 1},
        {x: 4, y: 4},
        {x: 5, y: 5}
      ];

      // Initialize the scatter plot for products tab
      var ctx = document.getElementById("productsScatterChart").getContext("2d");
      var productsScatterChart = new Chart(ctx, {
        type: "scatter",
        data: {
          datasets: [{
            label: "Sample Data",
            data: sampleScatterData,
            backgroundColor: "rgba(75, 192, 192, 0.6)",
            borderColor: "rgba(75, 192, 192, 1)"
          }]
        },
        options: {
          scales: {
            xAxes: [{
              type: 'linear',
              position: 'bottom',
              scaleLabel: {
                display: true,
                labelString: 'X Axis'
              }
            }],
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: 'Y Axis'
              }
            }]
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
