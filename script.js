const openPopupButtons = document.querySelectorAll('.open-popup');
const closePopupButtons = document.querySelectorAll('.close-popup');

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
