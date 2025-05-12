document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/summary")
    .then(response => response.json())
    .then(data => {
      console.log("Fetched data:", data);  // Log the response data
      document.getElementById("balance").textContent = `₹${data.balance.toFixed(2)}`;
      document.getElementById("income").textContent = data.income.toFixed(2);
      document.getElementById("expenses").textContent = data.expenses.toFixed(2);
    })
    .catch(err => {
      console.error("Failed to fetch summary:", err);
    });
});
