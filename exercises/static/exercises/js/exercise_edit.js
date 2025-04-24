// Exercise Edit JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the difficulty selector
    initializeDifficultySelector();

    // Preview functionality
    initializePreview();

    // Enhanced code editors
    enhanceCodeEditors();
});

function initializeDifficultySelector() {
    const difficultyOptions = document.querySelectorAll('.difficulty-option');

    difficultyOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Update the radio input
            const radioInput = this.querySelector('input[type="radio"]');
            radioInput.checked = true;

            // Update visual selection
            difficultyOptions.forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');
        });
    });
}

function initializePreview() {
    const previewBtn = document.getElementById('preview-btn');
    const previewContainer = document.getElementById('preview-container');
    const previewContent = document.getElementById('preview-content');

    if (previewBtn && previewContainer && previewContent) {
        previewBtn.addEventListener('click', function() {
            // Toggle preview visibility
            const isVisible = previewContainer.style.display !== 'none';

            if (isVisible) {
                previewContainer.style.display = 'none';
                previewBtn.textContent = 'Vista Previa';
            } else {
                // Get statement content and render preview
                const statementField = document.getElementById('id_statement');
                const titleField = document.getElementById('id_title');

                if (statementField && titleField) {
                    const title = titleField.value || 'Sin título';
                    const statement = statementField.value || 'Sin descripción';

                    // Simple markdown-like rendering for preview
                    const formattedStatement = statement
                        .replace(/\n\n/g, '</p><p>')
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em>$1</em>')
                        .replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');

                    previewContent.innerHTML = `
            <h4 style="margin-bottom: 1rem; color: var(--primary);">${title}</h4>
            <p>${formattedStatement}</p>
          `;

                    previewContainer.style.display = 'block';
                    previewBtn.textContent = 'Ocultar Vista Previa';

                    // Scroll to preview
                    previewContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    }
}

function enhanceCodeEditors() {
    const codeAreas = document.querySelectorAll('textarea.code-area');

    codeAreas.forEach(area => {
        // Add tab functionality
        area.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                e.preventDefault();

                // Insert tab at cursor position
                const start = this.selectionStart;
                const end = this.selectionEnd;

                this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);

                // Move cursor after the inserted tab
                this.selectionStart = this.selectionEnd = start + 4;
            }
        });

        // Auto-resize based on content
        area.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight + 2) + 'px';
        });

        // Initial sizing
        area.dispatchEvent(new Event('input'));
    });

    // Function name validation
    const functionNameInput = document.getElementById('id_function_name');
    const initialCodeArea = document.getElementById('id_initial_code');

    if (functionNameInput && initialCodeArea) {
        functionNameInput.addEventListener('blur', function() {
            const functionName = this.value.trim();
            if (functionName && initialCodeArea.value) {
                // Check if function name exists in the initial code
                if (!initialCodeArea.value.includes(`def ${functionName}`)) {
                    // Update the initial code with correct function name
                    let initialCode = initialCodeArea.value;

                    // Try to replace an existing function definition
                    const defRegex = /def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/;
                    const match = initialCode.match(defRegex);

                    if (match) {
                        initialCodeArea.value = initialCode.replace(
                            defRegex,
                            `def ${functionName}(`
                        );
                    } else {
                        // If no function definition found, add a template
                        initialCodeArea.value = `def ${functionName}():\n    return`;
                    }

                    // Show notification
                    showNotification('Código inicial actualizado con el nuevo nombre de función', 'info');
                }
            }
        });
    }
}

function showNotification(message, type = 'info') {
    // Check if notification container exists, create if not
    let notifContainer = document.getElementById('notification-container');

    if (!notifContainer) {
        notifContainer = document.createElement('div');
        notifContainer.id = 'notification-container';
        notifContainer.style.position = 'fixed';
        notifContainer.style.top = '20px';
        notifContainer.style.right = '20px';
        notifContainer.style.zIndex = '9999';
        document.body.appendChild(notifContainer);
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.backgroundColor = type === 'info' ? 'var(--primary-lighter)' : 'var(--secondary-light)';
    notification.style.color = type === 'info' ? 'var(--primary)' : '#b26f00';
    notification.style.padding = 'var(--space-md)';
    notification.style.borderRadius = 'var(--radius-md)';
    notification.style.marginBottom = 'var(--space-sm)';
    notification.style.boxShadow = 'var(--shadow-md)';
    notification.style.animation = 'slideInRight 0.3s ease-out forwards';
    notification.textContent = message;

    // Add to container
    notifContainer.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease-in forwards';
        setTimeout(() => {
            notifContainer.removeChild(notification);
        }, 300);
    }, 5000);
}

// Add CSS animations for notifications
const notificationStyles = `
@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}
`;

const styleElement = document.createElement('style');
styleElement.textContent = notificationStyles;
document.head.appendChild(styleElement);