const openPopupButtons = document.querySelectorAll('.open-popup');
const closePopupButtons = document.querySelectorAll('.close-popup');

window.onload = function() {
  fetch('https://raw.githubusercontent.com/TotoB12/TRIC/main/README.md')
    .then(response => response.text())
    .then(data => {
      document.getElementById('markdown-content').innerHTML = data;
    });
};

openPopupButtons.forEach(button => {
    button.addEventListener('click', () => {
        const popupId = button.getAttribute('data-popup');
        const popup = document.getElementById(popupId);
        popup.style.display = 'flex';
    });
});

closePopupButtons.forEach(button => {
    button.addEventListener('click', () => {
        const popup = button.closest('.popup');
        popup.style.display = 'none';
    });
});
