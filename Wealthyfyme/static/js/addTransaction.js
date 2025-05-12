document.addEventListener("DOMContentLoaded", function() {
    const addTransactionButton = document.getElementById('addTransactionBtn');
    const budgetsLink = document.getElementById('budgetsLink');
  
    addTransactionButton.addEventListener('click', function() {
      budgetsLink.click(); // Trigger the click on the Budgets link
    });
  });
  