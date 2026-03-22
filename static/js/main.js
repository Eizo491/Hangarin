document.addEventListener('DOMContentLoaded', () => {
    /**
     * STAGGERED FADE-IN ANIMATION
     * Applies the reveal class with a delay based on the card's index
     */
    const cards = document.querySelectorAll('.task-card');
    cards.forEach((card, index) => {
        card.classList.add('reveal-card');
        card.style.animationDelay = `${index * 0.1}s`;
    });

    /**
     * 3D TILT EFFECT
     * Targeted ONLY at dashboard cards. 
     * If your 'Create Task' container uses .task-card, change it to .task-form-container
     */
    const tiltElements = document.querySelectorAll('.task-card');
    
    tiltElements.forEach(el => {
        let glow = el.querySelector('.glow');
        if (!glow) {
            glow = document.createElement('div');
            glow.className = 'glow';
            el.appendChild(glow);
        }

        el.addEventListener('mousemove', (e) => {
            const rect = el.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top; 
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Reduced rotation intensity for a subtler feel
            const rotateX = (centerY - y) / 15;
            const rotateY = (x - centerX) / 15;

            el.style.setProperty('--x', `${x}px`);
            el.style.setProperty('--y', `${y}px`);

            el.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        el.addEventListener('mouseleave', () => {
            el.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)`;
        });
    });

    /**
     * MAGNETIC BUTTONS
     * Keeps the buttons feeling premium without moving the whole form
     */
    const magneticBtns = document.querySelectorAll('.btn-primary, .btn-light, .btn-white-solid');
    magneticBtns.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate3d(${x * 0.3}px, ${y * 0.5}px, 0) scale(1.05)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = `translate3d(0, 0, 0) scale(1)`;
            btn.style.transition = "all 0.4s cubic-bezier(0.23, 1, 0.32, 1)";
        });

        btn.addEventListener('mouseenter', () => {
            btn.style.transition = "none";
        });
    });

    /**
     * FORM SUBMISSION OVERLAY
     * Fixed centering logic for the Login/Signup views
     */
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            const overlay = document.createElement('div');
            overlay.className = 'loading-overlay d-flex align-items-center justify-content-center';
            
            // Inline styles to guarantee centering on top of everything
            Object.assign(overlay.style, {
                position: 'fixed',
                top: '0',
                left: '0',
                width: '100vw',
                height: '100vh',
                background: 'rgba(0, 0, 0, 0.4)',
                backdropFilter: 'blur(8px)',
                zIndex: '9999',
                opacity: '0',
                transition: 'opacity 0.3s ease'
            });

            overlay.innerHTML = '<div class="spinner-border text-light" style="width: 3rem; height: 3rem;" role="status"></div>';
            document.body.appendChild(overlay);
            
            // Force reflow for transition
            overlay.offsetHeight;
            overlay.style.opacity = '1';
        });
    });

    /**
     * AUTO-DISMISS ALERTS
     */
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            alert.style.transition = 'all 0.6s ease-out';
            setTimeout(() => alert.remove(), 600);
        }, 3500);
    });
});