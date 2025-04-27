const toggleBtn = document.getElementById('toggleBtn');
    const hiddenCards = document.querySelectorAll('.more-card');

    toggleBtn.addEventListener('click', function() {
      hiddenCards.forEach(card => {
        card.classList.toggle('d-none');
      });
      // Change button text based on the visibility of cards
      if (toggleBtn.textContent === 'Show More') {
        toggleBtn.textContent = 'Show Less';
      } else {
        toggleBtn.textContent = 'Show More';
      }
    });