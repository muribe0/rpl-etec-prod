// Course Details JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the accordion functionality for units
    initializeUnitAccordion();

    // Initialize any animations
    initializeAnimations();
});

function initializeUnitAccordion() {
    const unitHeaders = document.querySelectorAll('.unit-header');

    unitHeaders.forEach(header => {
        header.addEventListener('click', function() {
            const unit = this.parentElement;

            // Close all other units
            const allUnits = document.querySelectorAll('.unit');
            allUnits.forEach(otherUnit => {
                if (otherUnit !== unit && otherUnit.classList.contains('expanded')) {
                    otherUnit.classList.remove('expanded');
                }
            });

            // Toggle the current unit
            unit.classList.toggle('expanded');

            // Animate exercise items when a unit is expanded
            if (unit.classList.contains('expanded')) {
                const exerciseItems = unit.querySelectorAll('.exercise-item');
                animateExerciseItems(exerciseItems);
            }
        });
    });

    // Expand the first unit by default if there are units
    const firstUnit = document.querySelector('.unit');
    if (firstUnit) {
        firstUnit.classList.add('expanded');
        const exerciseItems = firstUnit.querySelectorAll('.exercise-item');
        animateExerciseItems(exerciseItems);
    }
}

function animateExerciseItems(items) {
    // Remove any existing animation classes
    items.forEach(item => {
        item.classList.remove('animate-fade-in-up');
    });

    // Add animations with a staggered delay
    items.forEach((item, index) => {
        setTimeout(() => {
            item.classList.add('animate-fade-in-up');
        }, index * 100); // 100ms delay between each item
    });
}

function initializeAnimations() {
    // Add any page load animations here
    const teacherControls = document.querySelector('.teacher-controls');
    if (teacherControls) {
        teacherControls.classList.add('fade-in');
    }
}

// Add hover effect for exercise items
document.addEventListener('mouseover', function(event) {
    const exerciseItem = event.target.closest('.exercise-item');
    if (exerciseItem) {
        exerciseItem.style.transform = 'translateY(-2px)';
        exerciseItem.style.transition = 'transform 0.2s ease';
    }
});

document.addEventListener('mouseout', function(event) {
    const exerciseItem = event.target.closest('.exercise-item');
    if (exerciseItem) {
        exerciseItem.style.transform = 'translateY(0)';
    }
});