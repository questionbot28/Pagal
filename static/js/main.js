// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return; // Skip empty hash links

        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.animate-on-scroll').forEach((element) => {
    observer.observe(element);
});

// Handle Discord auth UI
function updateAuthUI(user) {
    const authContainer = document.getElementById('auth-container');
    if (!authContainer) return;

    const loginBtn = document.getElementById('login-btn');
    const userProfile = authContainer.querySelector('.user-profile');

    if (user) {
        if (loginBtn) loginBtn.classList.add('d-none');
        if (userProfile) {
            userProfile.classList.remove('d-none');
            const avatar = userProfile.querySelector('.avatar');
            const username = userProfile.querySelector('.username');
            if (avatar) avatar.src = `https://cdn.discordapp.com/avatars/${user.id}/${user.avatar}.png`;
            if (username) username.textContent = user.username;
        }
    } else {
        if (loginBtn) loginBtn.classList.remove('d-none');
        if (userProfile) userProfile.classList.add('d-none');
    }
}

// Check auth status on page load
fetch('/api/user')
    .then(response => response.json())
    .then(user => {
        if (!user.error) {
            updateAuthUI(user);
        }
    })
    .catch(console.error);

// Update Discord invite links
document.querySelectorAll('a').forEach(link => {
    if (link.textContent.includes('Add to Discord') || link.textContent.includes('Add EduSphere')) {
        link.href = 'https://discord.com/oauth2/authorize?client_id=1159874534485262410&permissions=8&integration_type=0&scope=bot';
    } else if (link.textContent.includes('Join') || link.textContent.includes('Community')) {
        link.href = 'https://discord.gg/J3paY6YQkZ';
    }
});

// Typing animation for command preview
function typeWriter(element, text, speed = 50) {
    if (!element || !text) return;

    let i = 0;
    element.innerHTML = '';

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Initialize typing animations
document.addEventListener('DOMContentLoaded', () => {
    const commandElements = document.querySelectorAll('.command-preview');
    commandElements.forEach(element => {
        const text = element.getAttribute('data-text');
        if (text) {
            typeWriter(element, text);
        }
    });
});

// Mobile menu toggle
const toggleButton = document.querySelector('.navbar-toggler');
const navbarCollapse = document.querySelector('.navbar-collapse');

if (toggleButton && navbarCollapse) {
    toggleButton.addEventListener('click', () => {
        navbarCollapse.classList.toggle('show');
    });
}

// Header show/hide on scroll
let lastScroll = 0;
const header = document.querySelector('.navbar');

if (header) {
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll <= 0) {
            header.classList.remove('navbar-hidden');
            return;
        }

        if (currentScroll > lastScroll && !header.classList.contains('navbar-hidden')) {
            // Scroll down -> hide header
            header.classList.add('navbar-hidden');
        } else if (currentScroll < lastScroll && header.classList.contains('navbar-hidden')) {
            // Scroll up -> show header
            header.classList.remove('navbar-hidden');
        }

        lastScroll = currentScroll;
    });
}