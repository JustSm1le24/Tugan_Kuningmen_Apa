document.addEventListener('DOMContentLoaded', () => {
    // Scroll Animation
    const observerOptions = {
        threshold: 0.2
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-scroll').forEach(el => {
        observer.observe(el);
    });

    // Snowflake Animation
    const snowflakeContainer = document.getElementById('snowflakeContainer');
    const snowflakeCount = 30; // Increased count for snow effect
    const snowflakes = [];

    class Snowflake {
        constructor() {
            this.element = document.createElement('div');
            this.element.classList.add('snowflake');
            this.element.textContent = '❄️';
            snowflakeContainer.appendChild(this.element);
            this.reset();
        }

        reset() {
            this.x = Math.random() * window.innerWidth;
            this.y = -50 - Math.random() * window.innerHeight; // Start above screen
            this.speed = 1 + Math.random() * 2;
            this.sway = Math.random() * 0.1;
            this.swayOffset = Math.random() * Math.PI * 2;
            this.size = 10 + Math.random() * 20;

            this.element.style.fontSize = `${this.size}px`;
            this.element.style.opacity = 0.5 + Math.random() * 0.5;
        }

        update() {
            this.y += this.speed;
            this.x += Math.sin(this.y * 0.01 + this.swayOffset) * 0.5;

            // Reset if goes below screen
            if (this.y > window.innerHeight + 50) {
                this.reset();
            }

            this.element.style.transform = `translate(${this.x}px, ${this.y}px)`;
        }
    }

    for (let i = 0; i < snowflakeCount; i++) {
        snowflakes.push(new Snowflake());
    }

    function animateSnowflakes() {
        snowflakes.forEach(flake => flake.update());
        requestAnimationFrame(animateSnowflakes);
    }

    animateSnowflakes();
});
