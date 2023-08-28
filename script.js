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


const compareButton = document.getElementById('compare-button');

compareButton.addEventListener('click', () => {
    const file1 = document.getElementById('file1').value;
    const file2 = document.getElementById('file2').value;

    if (file1 !== 'Choose...' && file2 !== 'Choose...') {
        let popupContent = '';
        popupContent = '';
        if (file1 !== 'Run 1' && file2 !== 'Run 1') {
            popupContent = `
                    <h3>No Boom Run 1 vs Boom Run 1</h3>
                    <div class="row">
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_19-22-03.60 no boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_21-15-07.60 boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                    </div>
            `;
        } else if (file1 !== 'Run 2' && file2 !== 'Run 1') {
            popupContent = `
                    <h3>No Boom Run 2 vs Boom Run 1</h3>
                    <div class="row">
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_19-54-54.60 no boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_21-15-07.60 boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                    </div>
            `;
        } else if (file1 !== 'Run 1' && file2 !== 'Run 2') {
            popupContent = `
                    <h3>No Boom Run 1 vs Boom Run 2</h3>
                    <div class="row">
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_19-22-03.60 no boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_21-54-46.60 boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                    </div>
            `;
        } else if (file1 !== 'Run 2' && file2 !== 'Run 2') {
            popupContent = `
                    <h3>No Boom Run 2 vs Boom Run 2</h3>
                    <div class="row">
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_19-54-54.60 no boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                        <div class="col">
                            <iframe src="https://totob12.com/TRIC/final/2023-08-24_21-54-46.60 boom/graph.html" frameborder="0" marginheight="0" marginwidth="0" width="100%" height="100%" scrolling="auto"></iframe>
                        </div>
                    </div>
            `;
        }
        if (popupContent) {
            const popup = document.createElement('div');
            popup.classList.add('popup');
            popup.innerHTML = `
                <div class="popup-content">
                    <span class="close-popup">&times;</span>
                    ${popupContent}
                </div>
            `;
            document.body.appendChild(popup);
            popup.style.display = 'flex';

            const closeButton = popup.querySelector('.close-popup');
            closeButton.addEventListener('click', () => {
                popup.style.display = 'none';
            });
        }
    }
});

const compareButton2 = document.getElementById('compare-button2');

compareButton2.addEventListener('click', () => {
    const file11 = document.getElementById('file11').value;
    const file12 = document.getElementById('file12').value;

    if (file11 !== 'Choose...' && file12 !== 'Choose...') {
        let popupContent = '';
        popupContent = '';
        if (file11 !== 'Run 1' && file12 !== 'Run 1') {
            popupContent = `
                    <h3>No Boom Run 1 vs Boom Run 1</h3>
                    <iframe src="https://totob12.com/TRIC/final/noboomrun1boomrun1.html" frameborder="0"marginheight="0" marginwidth="0" width="100%" height="92%" scrolling="auto"></iframe>
            `;
        } else if (file11 !== 'Run 2' && file12 !== 'Run 1') {
            popupContent = `
                    <h3>No Boom Run 2 vs Boom Run 1</h3>
                    <iframe src="https://totob12.com/TRIC/final/noboomrun2boomrun1.html" frameborder="0"marginheight="0" marginwidth="0" width="100%" height="92%" scrolling="auto"></iframe>
            `;
        } else if (file11 !== 'Run 1' && file12 !== 'Run 2') {
            popupContent = `
                    <h3>No Boom Run 1 vs Boom Run 2</h3>
                    <iframe src="https://totob12.com/TRIC/final/noboomrun1boomrun2.html" frameborder="0"marginheight="0" marginwidth="0" width="100%" height="92%" scrolling="auto"></iframe>
            `;
        } else if (file11 !== 'Run 2' && file12 !== 'Run 2') {
            popupContent = `
                    <h3>No Boom Run 2 vs Boom Run 2</h3>
                    <iframe src="https://totob12.com/TRIC/final/noboomrun2boomrun2.html" frameborder="0"marginheight="0" marginwidth="0" width="100%" height="92%" scrolling="auto"></iframe>
            `;
        }
        if (popupContent) {
            const popup = document.createElement('div');
            popup.classList.add('popup');
            popup.innerHTML = `
                <div class="popup-content">
                    <span class="close-popup">&times;</span>
                    ${popupContent}
                </div>
            `;
            document.body.appendChild(popup);
            popup.style.display = 'flex';

            const closeButton = popup.querySelector('.close-popup');
            closeButton.addEventListener('click', () => {
                popup.style.display = 'none';
            });
        }
    }
});
