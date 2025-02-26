
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

document.getElementById('start-button').addEventListener('click', async function() {
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
    document.getElementById('refresh-country').style.display = 'block'

    document.getElementById('refresh-country').addEventListener('click', async function() {
        sendSignalToBackend('refresh');

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
        document.getElementById('result-message').innerText = ""; // Limpiar mensaje de resultado
    });

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
        } else {
            document.getElementById('result-message').innerText = `❌ Wrong! It was: ${result.correct_answer}`;
        }
    });

});



