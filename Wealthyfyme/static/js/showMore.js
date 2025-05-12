document.addEventListener('DOMContentLoaded', function () {
  const showMoreBtn = document.getElementById('showMoreCategories');

  if (showMoreBtn) {
    showMoreBtn.addEventListener('click', function () {
      const hiddenItems = document.querySelectorAll('.extra-category');
      hiddenItems.forEach(item => item.classList.remove('d-none'));
      showMoreBtn.style.display = 'none'; // hide the button after click
    });
  }
});
