// FlowMotion Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 1. Habit Response Handling (AJAX)
    const responseForms = document.querySelectorAll('.habit-response-form');
    
    responseForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const habitId = this.dataset.habitId;
            const url = this.action;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update streak
                    const streakElement = document.getElementById(`streak-${habitId}`);
                    if (streakElement) {
                        streakElement.innerText = data.current_streak;
                    }
                    
                    // Update UI status/actions
                    const statusContainer = document.getElementById(`status-${habitId}`);
                    if (statusContainer) {
                        statusContainer.innerHTML = '<span class="status-badge completed">✅ Completed</span>';
                    }
                    
                    const habitCard = this.closest('.habit-card');
                    if (habitCard) {
                        habitCard.classList.add('completed');
                    }
                    
                    // Show feedback (could use a toast library here)
                    if (data.feedback) {
                        console.log("Feedback:", data.feedback);
                        // Optional: alert(data.feedback);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback to normal form submission if AJAX fails
                form.submit();
            });
        });
    });
    
    // 2. Countdown Timers (Update every minute)
    updateAllCountdowns();
    setInterval(updateAllCountdowns, 60000);
});

function updateAllCountdowns() {
    const countdowns = document.querySelectorAll('.countdown-timer, #widget-countdown, .countdown');
    
    countdowns.forEach(el => {
        if (el.id === 'widget-countdown' || el.classList.contains('countdown')) {
            const startDateStr = el.getAttribute('data-start');
            const duration = parseInt(el.getAttribute('data-duration'));
            
            if (startDateStr && !isNaN(duration)) {
                const startDate = new Date(startDateStr);
                const today = new Date();
                
                // Reset hours to compare dates only
                const startDay = new Date(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());
                const currentDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
                
                const diffTime = currentDay - startDay;
                const daysPassed = Math.floor(diffTime / (1000 * 60 * 60 * 24));
                
                let remaining = duration - daysPassed;
                if (remaining < 0) remaining = 0;
                
                el.innerText = remaining;
                return;
            }
        }

        const targetTimeStr = el.getAttribute('data-time');
        if (!targetTimeStr) return;
        
        const [hours, minutes] = targetTimeStr.split(':');
        const now = new Date();
        const target = new Date();
        target.setHours(parseInt(hours), parseInt(minutes), 0);
        
        let diff = target - now;
        
        if (diff < 0) {
            target.setDate(target.getDate() + 1);
            diff = target - now;
        }
        
        displayTime(el, diff, false);
    });
}

function displayTime(element, diff, shortFormat) {
    const h = Math.floor(diff / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    
    if (shortFormat) {
        element.innerText = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')} remaining`;
    } else {
        element.innerText = `${h.toString().padStart(2, '0')}h ${m.toString().padStart(2, '0')}m remaining`;
    }
}
