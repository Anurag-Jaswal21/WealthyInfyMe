document.addEventListener("DOMContentLoaded", function () {
  setTimeout(() => {
    document.getElementById("loadingCard").style.display = "none";
    document.getElementById("featureCards").style.display = "flex";
  }, 1500); // Delay can be adjusted
});
