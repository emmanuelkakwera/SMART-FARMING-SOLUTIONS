// Main JavaScript file for Smart Farming Solutions

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'all 0.3s ease-out';
            message.style.transform = 'translateX(100%)';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                } else {
                    field.style.borderColor = '#e0e0e0';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('265')) {
                value = '+' + value;
            }
            e.target.value = value;
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Farm type dependent fields
    const farmTypeSelect = document.getElementById('farm_type');
    const cropsField = document.getElementById('main_crops');
    const livestockField = document.getElementById('livestock_types');

    if (farmTypeSelect) {
        farmTypeSelect.addEventListener('change', function() {
            const type = this.value;

            if (type === 'crops') {
                cropsField.closest('.form-group').style.display = 'block';
                livestockField.closest('.form-group').style.display = 'none';
            } else if (type === 'livestock') {
                cropsField.closest('.form-group').style.display = 'none';
                livestockField.closest('.form-group').style.display = 'block';
            } else if (type === 'mixed') {
                cropsField.closest('.form-group').style.display = 'block';
                livestockField.closest('.form-group').style.display = 'block';
            } else {
                cropsField.closest('.form-group').style.display = 'block';
                livestockField.closest('.form-group').style.display = 'block';
            }
        });

        // Trigger change event on page load
        farmTypeSelect.dispatchEvent(new Event('change'));
    }

    // Add loading states to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form.checkValidity()) {
                this.innerHTML = '<span class="loading-spinner">⏳</span> Processing...';
                this.disabled = true;
            }
        });
    });
});

// Utility functions
const SmartFarming = {
    // Format date
    formatDate: (dateString) => {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    },

    // Format number with commas
    formatNumber: (number) => {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },

    // Show notification
    showNotification: (message, type = 'info') => {
        const notification = document.createElement('div');
        notification.className = `flash-message ${type}`;
        notification.textContent = message;

        const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
        flashContainer.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 5000);
    }
};

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}