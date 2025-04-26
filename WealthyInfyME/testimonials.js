document.addEventListener("DOMContentLoaded", function() {
  const navbar = document.querySelector('.custom-navbar');
  const testimonialsSection = document.getElementById('testimonials');

  const observer = new IntersectionObserver(
    function(entries) {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navbar.classList.add('in-testimonials');
        } else {
          navbar.classList.remove('in-testimonials');
        }
      });
    }, 
    { threshold: 0.5 } // Adjust depending on when you want it to trigger (50% visible here)
  );

  observer.observe(testimonialsSection);
});
