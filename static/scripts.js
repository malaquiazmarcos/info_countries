
/**
 * Obtain the token CSRF of browser cookies.
 * 
 * This function search the cookie called 'csrftoken', extract value and return
 * common using in Django aplication to protect attacks CSRF in requests AJAX.
 * 
 * @returns {string|null} the value token if found or null. 
 */
function getCSRFToken() {
    let cookieValue = null;
    let cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith('csrftoken=')) {
            cookieValue = cookie.split('=')[1];
            break;
        }
    }

    return cookieValue;
}

/**
 * Send an specific signal to backend.
 * 
 * Main useing for send a signal to Django, and make an action.
 * 
 * @param {string} action - A string to send (e.g. 'refresh').
 */
async function sendSignalToBackend(action) {
    let formData = new FormData()
    formData.append('action',action)

    let response = await fetch('/guess-the-country/', {
        method: 'POST',
        headers:{
            'X-CSRFToken': getCSRFToken()
        },
        body: formData
    });
    
    let result = await response.json()
    console.log(`Server response for ${action}:`, result)
}

let nameCountryName = '';

/**
 * Initializes the game by fetching a random country.
 * Hidden the button start and show the country and flag.
 * Show imput and button refresh.
 */
document.getElementById('start-button').addEventListener('click', async function() {
    document.getElementById('country-input').value = '';
    
    let response = await fetch('/guess-the-country/', {
        'headers': {'X-Requested-With': 'XMLHttpRequest'}
    });
    let data = await response.json()
    console.log('Country:', data.name)
    console.log('Flag:', data.flags)

    currentCountryName = data.name;

    document.getElementById('start-button').style.display = 'none';

    document.getElementById('random-country').innerHTML = `
    <p>Country: ${data.name}</p>
    <img src="${data.flags}">
    `;

    document.getElementById('input-div').style.display = 'block';
    document.getElementById('refresh-country').style.display = 'block'

    /**
     * Refresh the guess, show again a new country and flag.
     */
    document.getElementById('refresh-country').addEventListener('click', async function() {
        sendSignalToBackend('refresh');
        document.getElementById('country-input').value = '';

        let response = await fetch('/guess-the-country/', {
            'headers': {'X-Requested-With': 'XMLHttpRequest'}
        });
        let data = await response.json()
        console.log('Country:', data.name)
        console.log('Flag:', data.flags)
    
        document.getElementById('start-button').style.display = 'none';
    
        document.getElementById('random-country').innerHTML = `
        <p>Country: ${data.name}</p>
        <img src="${data.flags}">
        `;

        document.getElementById('input-div').style.display = 'block';
        document.getElementById('result-message').innerText = '';
        document.getElementById('data-country').innerHTML = '';
    });

    /**
     * Send user responde to backend to verify if correct or not. 
     */
    document.getElementById('submit-button').addEventListener('click', async function() {
        let userGuess = document.getElementById('country-input').value;

        console.log("📤 Enviando:", userGuess);
    
        let response = await fetch('/guess-the-country/', { 
            method:'POST', 
            headers:{
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCSRFToken()
            },
            body: `country-input=${encodeURIComponent(userGuess)}`
        });
        let result = await response.json();
        console.log(result)
    
        if (result.correct) {
            document.getElementById('result-message').innerText = '✅ Correct!';
            document.getElementById('input-div').style.display = 'none';
            document.getElementById('data-country').innerHTML = 
                `<a href="/buscar-pais-por-nombre/?name=${encodeURIComponent(result.correct_answer)}">Learn more about ${result.correct_answer}</a>`;
        } else {
            document.getElementById('result-message').innerText = `❌ Wrong! It was: ${result.correct_answer}`;
            document.getElementById('data-country').innerHTML = 
                `<a href="/buscar-pais-por-nombre/?name=${encodeURIComponent(result.correct_answer)}">Learn more about ${result.correct_answer}</a>`;
        }
    });

});





