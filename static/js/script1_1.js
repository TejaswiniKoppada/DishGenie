
  
  // Logout Button
  document.getElementById("logout-btn").addEventListener("click", () => {
    alert("Logged out successfully!");
    // Redirect to login page or perform logout logic
  });


  let slideIndex = 0;
const slides = document.querySelectorAll(".slide");
const dotsContainer = document.querySelector(".dots-container");

// Create dots dynamically
slides.forEach((_, index) => {
    const dot = document.createElement("span");
    dot.classList.add("dot");
    dot.setAttribute("onclick", `currentSlide(${index})`);
    dotsContainer.appendChild(dot);
});

const dots = document.querySelectorAll(".dot");

function showSlides(index) {
    if (index >= slides.length) slideIndex = 0;
    if (index < 0) slideIndex = slides.length - 1;

    slides.forEach(slide => (slide.style.display = "none"));
    dots.forEach(dot => dot.classList.remove("active"));

    slides[slideIndex].style.display = "block";
    dots[slideIndex].classList.add("active");
}

// Auto slide every 3 seconds
function autoSlide() {
    moveSlide(1);
    setTimeout(autoSlide, 3000);
}

// Move slide manually
function moveSlide(n) {
    slideIndex += n;
    showSlides(slideIndex);
}

// Navigate to a specific slide
function currentSlide(n) {
    slideIndex = n;
    showSlides(slideIndex);
}

// Initialize carousel
showSlides(slideIndex);
setTimeout(autoSlide, 3000);
        // Add an event listener to the logout button
        document.getElementById('logout-btn').addEventListener('click', function() {
            // Make a request to the /logout route
            fetch('/logout', {
                method: 'GET',
            })
            .then(response => {
                if (response.redirected) {
                    // Redirect to the first.html page
                    window.location.href = response.url;
                }
            })
            .catch(error => {
                console.error('Error during logout:', error);
            });
        });

        // Function to check if an element is in the viewport
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }

        // Function to add visible class when scrolled into view
        function handleScroll() {
            const sections = document.querySelectorAll('.section');
            sections.forEach(section => {
                if (isInViewport(section)) {
                    section.classList.add('visible');
                }
            });
        }

        // Add scroll event listener
        window.addEventListener('scroll', handleScroll);

        // Trigger handleScroll on page load
        document.addEventListener('DOMContentLoaded', () => {
            handleScroll();
        });