function fade(el) {
    el.style.opacity = 1;
    var last = +new Date();
    var tick = function() {
        el.style.opacity = +el.style.opacity - (new Date() - last) / 400;
        last = +new Date();

        if (+el.style.opacity > 0) {
            (window.requestAnimationFrame && requestAnimationFrame(tick)) || setTimeout(tick, 16);
        }
    };
    tick();
}

function fade_out_messages() {
    const messages_container = document.querySelector('#messages-container');

    const progress = document.querySelector('.message__progress');
    if (progress) {
        progress.addEventListener('animationend', () => {
            fade(messages_container);
            messages_container.style.pointerEvents = 'none';
        });
    }
}

function close_messages() {
    const messages_container = document.querySelector('#messages-container');
    if (!messages_container) return;
    const close_buttons = messages_container.querySelectorAll('.message__close');

    close_buttons.forEach(button => {
        button.addEventListener('click', () => {
            const message = button.parentElement.parentElement.parentElement.parentElement;
            fade(message);
            this.setTimeout(() => {
                message.style.display = 'none';
            }, { delay: 1000 });
        }, { once: true });
    });
}
document.addEventListener('DOMContentLoaded', function() {

    // Fade out messages
    fade_out_messages();

    // Close messages
    close_messages();
});





