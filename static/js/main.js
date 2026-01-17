document.addEventListener('DOMContentLoaded', function() {
    const quickResponds = document.querySelectorAll('.quick-respond');
    quickResponds.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            
            fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const card = form.closest('.habit-card');
                    card.classList.add('completed');
                    
                    const actions = card.querySelector('.habit-actions');
                    actions.innerHTML = '<span class="completed-badge">Completed</span>' +
                        actions.querySelector('.btn-outline').outerHTML;
                    
                    const streakEl = card.querySelector('.habit-streak');
                    if (streakEl) {
                        streakEl.textContent = 'Streak: ' + data.current_streak + ' days';
                    }
                }
            })
            .catch(err => {
                form.submit();
            });
        });
    });
});
