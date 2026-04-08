// Function to save task to LocalStorage when offline
function saveTaskOffline(taskData) {
    let queue = JSON.parse(localStorage.getItem('offlineTaskQueue') || '[]');
    queue.push(taskData);
    localStorage.setItem('offlineTaskQueue', JSON.stringify(queue));
    
    alert("You are offline! Hangarin saved this task locally and will sync it automatically when you're back online.");
}

// Function to sync the queue back to Django
async function syncOfflineTasks() {
    if (!navigator.onLine) return;

    let queue = JSON.parse(localStorage.getItem('offlineTaskQueue') || '[]');
    if (queue.length === 0) return;

    console.log("Internet restored! Syncing tasks...");

    for (const task of queue) {
        try {
            const response = await fetch('/task/create/', { // Match your URL name
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(task)
            });
            if (response.ok) {
                console.log("Task synced successfully!");
            }
        } catch (error) {
            console.error("Sync failed for a task:", error);
        }
    }
    // Clear the queue after successful sync
    localStorage.removeItem('offlineTaskQueue');
}

// Check for sync every time the browser comes back online
window.addEventListener('online', syncOfflineTasks);

// Helper to get Django CSRF Token
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