function searchCustomer() {
    var customerId = document.getElementById('search-input').value;
    fetch(`/search?customer_id=${customerId}`)
      .then(response => response.json())
      .then(data => {
        var resultsContainer = document.getElementById('search-results');
        if (data.success) {
          // Nhân các giá trị với 100 và làm tròn đến 2 chữ số thập phân để hiển thị dưới dạng phần trăm
          var pdPercentage = (data.pd * 100).toFixed(2);
          var lgdPercentage = (data.lgd * 100).toFixed(2);

          resultsContainer.innerHTML = `
            <div class="data-card">
              <h2>Customer Details</h2>
              <div><strong>Customer ID:</strong> ${customerId}</div>
              <div><strong>Funded Amount:</strong> $${parseFloat(data.funded_amnt).toFixed(2)}</div>
              <div><strong>Probability of Default (PD):</strong> ${pdPercentage}%</div>
              <div><strong>Loss Given Default (LGD):</strong> ${lgdPercentage}%</div>
              <div><strong>Exposure at Default (EAD):</strong> $${parseFloat(data.ead).toFixed(2)}</div>
              <div><strong>Expected Loss (EL):</strong> $${parseFloat(data.el).toFixed(2)}</div>
              <button class="print-button" onclick="printCustomerDetails()">Print</button>
            </div>`;
        } else {
          resultsContainer.innerHTML = `<div>No customer found with ID ${customerId}</div>`;
        }
      })
      .catch(error => console.error('Error:', error));
}


function printCustomerDetails() {
    var content = document.getElementById('search-results').innerHTML;
    var printWindow = window.open('', '', 'height=600,width=800');
    printWindow.document.write('<html><head><title>Customer Credit Details</title>');
    printWindow.document.write('<style>');
    printWindow.document.write(`
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #fff;
            color: #333;
        }
        .data-card {
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .data-card h2 {
            color: #444;
            font-size: 24px;
            border-bottom: 2px solid #666;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .data-card div {
            font-size: 16px;
            margin-bottom: 10px;
        }
        .print-button { display: none; }
    `);
    printWindow.document.write('</style>');
    printWindow.document.write('</head><body>');
    printWindow.document.write(content);
    printWindow.document.write('</body></html>');
    printWindow.document.close();
    printWindow.print();
}
