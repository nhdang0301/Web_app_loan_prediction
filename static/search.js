document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('search-input');
  input.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
      event.preventDefault();  // Prevent the default form submission
      searchCustomer();  // Trigger the search function
    }
  });
});

function searchCustomer() {
  const customerId = document.getElementById('search-input').value.trim();
  fetch(`/search?customer_id=${encodeURIComponent(customerId)}`)
    .then(response => response.json())
    .then(data => {
      const resultsContainer = document.getElementById('search-results');
      const chartContainer = document.getElementById('resultChart');
      if (data.success) {
        resultsContainer.innerHTML = `
          <div class="data-card">
            <h2>Customer Details</h2>
            <div><strong>Customer ID:</strong> ${customerId}</div>
            <div><strong>Funded Amount:</strong> $${parseFloat(data.funded_amnt).toFixed(2)}</div>
            <div><strong>Probability of Default (PD):</strong> ${parseFloat(data.pd * 100).toFixed(2)}%</div>
            <div><strong>Loss Given Default (LGD):</strong> ${parseFloat(data.lgd * 100).toFixed(2)}%</div>
            <div><strong>Exposure at Default (EAD):</strong> $${parseFloat(data.ead).toFixed(2)}</div>
            <div><strong>Expected Loss (EL):</strong> $${parseFloat(data.el).toFixed(2)}</div>
            <button class="print-button" onclick="printCustomerDetails()">Print</button>
          </div>`;
        // Display the chart container
        chartContainer.style.display = 'block';
        updateChart(data);
      } else {
        resultsContainer.innerHTML = `<div>No customer found with ID ${customerId}</div>`;
        chartContainer.style.display = 'none';  // Hide the chart if no data
      }
    })
    .catch(error => {
      console.error('Error:', error);
      resultsContainer.innerHTML = `<div>Error fetching customer details. Please try again.</div>`;
    });
}

function updateChart(data) {
  const ctx = document.getElementById('resultChart').getContext('2d');
  // Destroy the previous chart if exists
  if (window.resultChart) window.resultChart.destroy();
  window.resultChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Expected Loss'],
      datasets: [{
        label: 'Expected Loss',
        data: [data.el],
        backgroundColor: ['rgba(54, 162, 235, 0.2)'],
        borderColor: ['rgba(54, 162, 235, 1)'],
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function printCustomerDetails() {
  const content = document.getElementById('search-results').innerHTML;
  const printWindow = window.open('', '', 'height=600,width=800');
  printWindow.document.write(`
    <html><head><title>Customer Credit Details</title><style>
      body { font-family: 'Arial', sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #fff; color: #333; }
      .data-card { border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 20px; padding: 20px; background-color: #f9f9f9; }
      .data-card h2 { color: #444; font-size: 24px; border-bottom: 2px solid #666; padding-bottom: 10px; margin-bottom: 20px; }
      .data-card div { font-size: 16px; margin-bottom: 10px; }
      .print-button { display: none; }
    </style></head><body>${content}</body></html>`);
  printWindow.document.close();
  printWindow.print();
}
