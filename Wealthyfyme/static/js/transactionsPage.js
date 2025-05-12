document.getElementById('transactionsLink').addEventListener('click', function (e) {
    e.preventDefault();
    fetch('/transactions') // Flask route for transaction.html
      .then(response => response.text())
      .then(html => {
        const mainContent = document.getElementById('main-content');
        mainContent.innerHTML = html;
      })
      .catch(error => {
        console.error('Error loading transactions:', error);
      });
  });