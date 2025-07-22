// Student Planner JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Task status update functionality
    initializeTaskStatusUpdates();

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s';
                alert.style.opacity = '0';
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.length <= 1) return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Initialize task status update functionality
function initializeTaskStatusUpdates() {
    document.querySelectorAll('.task-status-select').forEach(function(select) {
        select.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const newStatus = this.value;
            const row = this.closest('tr');
            const taskCard = this.closest('.task-card');
            
            updateTaskStatus(taskId, newStatus, row, taskCard);
        });
    });
}

// Function to update task status via AJAX
function updateTaskStatus(taskId, newStatus, row, taskCard) {
    fetch(`/tasks/${taskId}/status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: `status=${newStatus}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI based on context (task list or dashboard)
            if (row) {
                // Update in task list view
                const statusBadge = row.querySelector('td:nth-child(4) .badge:first-child');
                const statusText = row.querySelector('.task-status-select option:checked').text;
                
                if (statusBadge) {
                    statusBadge.textContent = statusText;
                    statusBadge.className = 'badge ' + getStatusBadgeClass(newStatus);
                }
            }
            
            if (taskCard) {
                // Update in dashboard view
                taskCard.className = `task-card ${newStatus} mb-3 p-3`;
            }
            
            showNotification('Status updated successfully!', 'success');
        } else {
            showNotification('Error updating status.', 'danger');
        }
    })
    .catch(() => {
        showNotification('An error occurred while updating status.', 'danger');
    });
}

// Helper function to get badge class based on status
function getStatusBadgeClass(status) {
    switch (status) {
        case 'done':
            return 'bg-success';
        case 'in_progress':
            return 'bg-info';
        default:
            return 'bg-warning';
    }
}

// Function to show notifications
function showNotification(message, type = 'info') {
    const alertClass = type === 'success' ? 'alert-success' : 
                      type === 'error' ? 'alert-danger' : 'alert-info';
    
    const notification = document.createElement('div');
    notification.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Function to get CSRF token from cookies
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

// Function to confirm deletions
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// Function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Function to format times
function formatTime(timeString) {
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
} 