document.getElementById('loanPredictionForm').addEventListener('submit', function(e) {
    e.preventDefault(); // Prevent the default form submission
    
    // Retrieve form values
    const loanAmount = document.getElementById('loanAmount').value;
    const income = document.getElementById('income').value;
    const creditScore = document.getElementById('creditScore').value;
    
    // For demonstration, just log the values to the console
    console.log(`Loan Amount: ${loanAmount}, Income: ${income}, Credit Score: ${creditScore}`);
    
    // Here, you would typically send the data to your server or API for prediction
    // For now, just show a simple alert
    alert('Prediction submitted. Check the console for values.');
});
