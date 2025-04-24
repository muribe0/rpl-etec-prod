document.addEventListener('DOMContentLoaded', function() {
    // Handle tab key in textarea
    const codeTextarea = document.querySelector('#id_code');
    if (codeTextarea) {
        codeTextarea.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();

                // Insert 4 spaces at cursor position
                const start = this.selectionStart;
                const end = this.selectionEnd;

                // Set textarea value to: text before cursor + 4 spaces + text after cursor
                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);

                // Move cursor after the inserted spaces
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });
    }

    // Toggle visibility of previous submissions
    const togglePreviousBtn = document.querySelector('#toggle-previous-btn');
    const previousSubmissions = document.querySelector('#previous-submissions');

    if (togglePreviousBtn && previousSubmissions) {
        togglePreviousBtn.addEventListener('click', function() {
            const isHidden = previousSubmissions.classList.toggle('hidden');
            togglePreviousBtn.textContent = isHidden ? 'Show Previous Attempts' : 'Hide Previous Attempts';
        });
    }

    // Enhance difficulty display
    const difficultyElement = document.querySelector('#exercise-difficulty');
    if (difficultyElement) {
        const difficulty = parseInt(difficultyElement.dataset.difficulty || 1);
        const maxDifficulty = 5;

        let difficultyHtml = '';
        for (let i = 1; i <= maxDifficulty; i++) {
            const activeClass = i <= difficulty ? 'active' : '';
            difficultyHtml += `<span class="difficulty-dot ${activeClass}"></span>`;
        }

        difficultyElement.innerHTML = difficultyHtml;
    }

    // Make code editor resizable
    const codeEditor = document.querySelector('.exercise-code-editor');
    if (codeEditor) {
        const resizeObserver = new ResizeObserver(() => {
            // When the editor is resized, also resize the results container
            const resultsContainer = document.querySelector('#results-container');
            if (resultsContainer) {
                resultsContainer.style.maxHeight = `${Math.max(300, codeEditor.offsetHeight)}px`;
            }
        });

        resizeObserver.observe(codeEditor);
    }
});