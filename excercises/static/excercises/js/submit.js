function addSubmitListener() {
    const form = document.querySelector('#submit-code-form');
    form.onsubmit = () => {

        // Disable the submit button for now. Later we will enable more submissions.
        const btn = form.querySelector('#submit-btn');
        // btn.disabled = true;

        // Run tests by sending a request to the server.

        sendCode();

        return false;
    };
}

function displayMessage(test_results) {
    const results_container = document.querySelector('#results-container');
    const title = results_container.querySelector('#results-title');
    const code = results_container.querySelector("#results-test");
    title.innerHTML = 'Resultados:';
    code.innerHTML = test_results;
}

function hideLoadingOverlay() {
    const loadingOverlay = document.querySelector('#loading-overlay');
    loadingOverlay.innerHTML = '';
}

function showLoadingOverlay() {
    const loadingOverlay = document.querySelector('#loading-overlay');
    loadingOverlay.innerHTML = 'Loading...';
}

function sendCode() {
    /*
    Sends a POST request to the server with the code to be tested.
    Displays a loading overlay while the tests are running.
     */
    const code = document.querySelector('#id_code').value;
    showLoadingOverlay();

    fetch(`/submit/`, {
        method: 'POST',
        body: JSON.stringify({
            code: code,
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log("Submitted code. Task ID:", data['task_id']);
            readTestResults(data['task_id']);
        })
        .catch(error => {
            console.error('Fetching Error:', error);
        })

}

function readTestResults(task_id) {
    /*
    Check the results of the tests, when available display them modifying the DOM.
    Hide the loading overlay.
     */
    fetch(`/results/${task_id}`)
        .then(response => response.json())
        .then(data => {
            console.log("Checking results...");
            displayMessage(data['results']);
            hideLoadingOverlay();
        })
        .catch(error => {
            console.error('Fetching Error:', error);
        });
}


function main() {
    addSubmitListener();
}


document.addEventListener('DOMContentLoaded', main);
