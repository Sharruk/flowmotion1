// FlowMotion Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // 1. Habit Response Handling (AJAX)
    const responseForms = document.querySelectorAll('.habit-response-form, .response-form');
    
    responseForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitter = e.submitter;
            if (submitter && (submitter.value === 'yes' || submitter.value === 'no' || this.classList.contains('habit-response-form'))) {
                e.preventDefault();
                
                const formData = new FormData(this);
                if (submitter && submitter.name === 'completed') {
                    formData.set('completed', submitter.value);
                }
                
                const habitId = this.dataset.habitId || window.location.pathname.split('/')[2];
                const url = this.action;
                
                fetch(url, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        location.reload(); 
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    this.submit();
                });
            }
        });
    });
    
    // 2. Countdown Timers
    updateAllCountdowns();
    setInterval(updateAllCountdowns, 1000); // Live update every second
});

function updateAllCountdowns() {
    const countdowns = document.querySelectorAll('.countdown-timer, #widget-countdown, .countdown');
    
    countdowns.forEach(el => {
        // Dynamic day-based calculation for widgets
        const startDateStr = el.getAttribute('data-start');
        const duration = parseInt(el.getAttribute('data-duration'));
        const serverTimeStr = el.getAttribute('data-server-time');
        
        if (startDateStr && !isNaN(duration)) {
            const startDate = new Date(startDateStr);
            // Use server time as base to prevent client skew
            const baseTime = serverTimeStr ? new Date(serverTimeStr) : new Date();
            
            const startDay = Date.UTC(startDate.getFullYear(), startDate.getMonth(), startDate.getDate());
            const currentDay = Date.UTC(baseTime.getFullYear(), baseTime.getMonth(), baseTime.getDate());
            
            const diffTime = currentDay - startDay;
            const daysPassed = Math.floor(diffTime / (1000 * 60 * 60 * 24));
            
            let remaining = duration - daysPassed;
            if (remaining < 0) remaining = 0;
            
            el.innerText = remaining;
            return;
        }

        // Live time-based calculation for reminders
        const targetTimeStr = el.getAttribute('data-time');
        if (!targetTimeStr) return;
        
        const [hours, minutes] = targetTimeStr.split(':');
        const now = new Date();
        const target = new Date();
        target.setHours(parseInt(hours), parseInt(minutes), 0);
        
        if (target < now) {
            target.setDate(target.getDate() + 1);
        }
        
        const diff = target - now;
        const h = Math.floor(diff / 3600000);
        const m = Math.floor((diff % 3600000) / 60000);
        const s = Math.floor((diff % 60000) / 1000);
        
        if (el.id === 'widget-countdown' || el.classList.contains('countdown')) {
             // If we have a time-based widget (like in widget.html)
             el.innerText = `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        } else {
             el.innerText = `${h.toString().padStart(2, '0')}h ${m.toString().padStart(2, '0')}m ${s.toString().padStart(2, '0')}s remaining`;
        }
    });
}

function acknowledgeHabit(habitId) {
    fetch(`/habits/${habitId}/acknowledge/`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
