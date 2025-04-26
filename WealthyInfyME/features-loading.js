document.addEventListener("DOMContentLoaded", function () {
  // Simulate loading delay
  setTimeout(() => {
    document.getElementById("loadingCard").style.display = "none";
    document.getElementById("featureCards").style.display = "flex";
  }, 1500); // 1.5 second delay
});
