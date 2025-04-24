// Main JavaScript for animations and interactions
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const navbarToggle = document.querySelector('.navbar-toggle');
    const navbarNav = document.querySelector('.navbar-nav');

    if (navbarToggle && navbarNav) {
        navbarToggle.addEventListener('click', function() {
            navbarNav.classList.toggle('open');
            // Update aria-expanded attribute for accessibility
            const isExpanded = navbarNav.classList.contains('open');
            navbarToggle.setAttribute('aria-expanded', isExpanded);
        });
    }

    // Handle closing messages
    initializeMessageSystem();

    // Add animation to course cards - with simpler approach
    animateCourseCardsSimple();
});

function initializeMessageSystem() {
    // Get all message close buttons
    const closeButtons = document.querySelectorAll('.message__close');

    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Find the parent message element
            const message = this.closest('.message');

            // Add fade-out animation
            message.style.animation = 'fadeOut 0.3s ease-in-out forwards';

            // Remove the message after animation completes
            setTimeout(() => {
                message.remove();
            }, 300);
        });
    });

    // Auto dismiss messages after the progress bar completes
    const messages = document.querySelectorAll('.message');

    messages.forEach(message => {
        const progressBar = message.querySelector('.message__progress');

        if (progressBar) {
            // Listen for when the progress animation ends
            progressBar.addEventListener('animationend', () => {
                // Add fade-out animation
                message.style.animation = 'fadeOut 0.3s ease-in-out forwards';

                // Remove the message after animation completes
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
    });
}

function animateCourseCardsSimple() {
    // Simpler animation that won't hide the cards
    const cards = document.querySelectorAll('.course-card');

    // Add a small delay between each card
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100); // 100ms delay between each card
    });
}

// Add fade-out animation for messages
const fadeOutKeyframes = `
@keyframes fadeOut {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}`;

// Add the keyframes to the document
const style = document.createElement('style');
style.textContent = fadeOutKeyframes;
document.head.appendChild(style);