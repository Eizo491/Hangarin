/**
 * Hangarin Productivity Suite - main.js
 */

document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. TASK DETAIL SIDEBAR LOGIC ---
    const taskRows = document.querySelectorAll('.task-row');
    const sidebar = {
        title: document.getElementById('detailTitle'),
        desc: document.getElementById('detailDesc'),
        category: document.getElementById('detailCategory'),
        priority: document.getElementById('detailPriority'),
        deadline: document.getElementById('detailDeadline'),
        editBtn: document.getElementById('detailEditLink'),
        deleteBtn: document.getElementById('detailDeleteLink')
    };

    taskRows.forEach(row => {
        row.addEventListener('click', function() {
            const data = {
                id: this.getAttribute('data-id'),
                title: this.getAttribute('data-title'),
                desc: this.getAttribute('data-desc') || "No description provided.",
                cat: this.getAttribute('data-cat') || 'General',
                pri: this.getAttribute('data-pri'),
                deadline: this.getAttribute('data-deadline')
            };

            if(sidebar.title) sidebar.title.innerText = data.title;
            if(sidebar.desc) sidebar.desc.innerText = data.desc;
            if(sidebar.category) sidebar.category.innerHTML = `<i class="fas fa-tag me-1"></i> ${data.cat}`;
            if(sidebar.deadline) sidebar.deadline.innerText = data.deadline;
            
            // Dynamic URLs for Django
            if(sidebar.editBtn) sidebar.editBtn.href = `/task/update/${data.id}/`; 
            if(sidebar.deleteBtn) sidebar.deleteBtn.href = `/task/delete/${data.id}/`;

            if(sidebar.priority) updatePriorityBadge(sidebar.priority, data.pri);
        });
    });

    function updatePriorityBadge(element, priority) {
        element.className = 'badge rounded-pill border px-3 ';
        switch(priority) {
            case 'Critical':
                element.classList.add('bg-danger', 'text-white');
                element.innerHTML = `<i class="fas fa-fire me-1"></i> Critical`;
                break;
            case 'High':
                element.classList.add('bg-light', 'text-danger', 'border-danger');
                element.innerHTML = `<i class="fas fa-circle me-1"></i> High`;
                break;
            case 'Medium':
                element.classList.add('bg-light', 'text-warning', 'border-warning');
                element.innerHTML = `<i class="fas fa-circle me-1"></i> Medium`;
                break;
            case 'Low':
                element.classList.add('bg-light', 'text-info', 'border-info');
                element.innerHTML = `<i class="fas fa-circle me-1"></i> Low`;
                break;
            case 'Optional':
                element.classList.add('bg-light', 'text-muted');
                element.innerHTML = `<i class="fas fa-circle-notch me-1"></i> Optional`;
                break;
        }
    }

    // --- 2. PREMIUM ANIMATIONS (Tilt & Stagger) ---
    const revealElements = document.querySelectorAll('.card, .animate-view');
    revealElements.forEach((el, index) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition = "all 0.6s cubic-bezier(0.23, 1, 0.32, 1)";
        setTimeout(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }, index * 100);
    });

    const tiltCards = document.querySelectorAll('.card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const rotateX = (rect.height / 2 - y) / 20;
            const rotateY = (x - rect.width / 2) / 20;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });

    // --- 3. MAGNETIC BUTTONS ---
    const magneticBtns = document.querySelectorAll('.btn-primary, .btn-outline-primary');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate3d(${x * 0.2}px, ${y * 0.4}px, 0) scale(1.05)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = `translate3d(0, 0, 0) scale(1)`;
        });
    });

    // --- 4. GLOBAL FORM OVERLAY & OFFLINE INTERCEPTION ---
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            // Check if we are on the Task Form and if we are Offline
            if (form.id === 'taskForm' && !navigator.onLine) {
                e.preventDefault(); // Stop page refresh
                
                // Get data from your widget_tweak fields
                const taskData = {
                    title: document.getElementById('id_title')?.value,
                    description: document.getElementById('id_description')?.value,
                    category: document.getElementById('id_category')?.value,
                    priority: document.getElementById('id_priority')?.value,
                    status: document.getElementById('id_status')?.value,
                    deadline: document.getElementById('id_deadline')?.value
                };

                // Save to local queue using handler.js function
                if (typeof saveTaskOffline === "function") {
                    saveTaskOffline(taskData);
                    form.reset();
                }
                return; // Don't show the loading overlay if we're offline
            }

            // Normal Online Overlay Logic
            const overlay = document.createElement('div');
            Object.assign(overlay.style, {
                position: 'fixed', top: '0', left: '0', width: '100%', height: '100%',
                background: 'rgba(255, 255, 255, 0.7)', backdropFilter: 'blur(5px)',
                zIndex: '10000', display: 'flex', alignItems: 'center', justifyContent: 'center'
            });
            overlay.innerHTML = '<div class="spinner-border text-primary" role="status"></div>';
            document.body.appendChild(overlay);
        });
    });

    // --- 5. ALERT AUTO-CLOSE ---
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500);
        }, 3000);
    });
});