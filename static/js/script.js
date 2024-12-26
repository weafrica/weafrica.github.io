let slideIndex = 0; // Initialize the slide index to 0
showSlides(); // Call the function to display the slides

function showSlides() {
    let slides = document.getElementsByClassName("slide"); // Get all elements with class "slide"
    let dots = document.getElementsByClassName("dot"); // Get all elements with class "dot"

    // Hide all slides initially
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }

    slideIndex++; // Increment the slide index

    // If the slide index exceeds the number of slides, reset it to 1
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }

    // Show 3 slides at a time
    for (let i = 0; i < 3; i++) {
        let index = (slideIndex + i - 1) % slides.length; // Calculate the current slide index
        slides[index].style.display = "block"; // Display the current slide
    }

    // Remove the "active" class from all dots
    for (let i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    // Add the "active" class to the current dot
    dots[(slideIndex - 1) % dots.length].className += " active";

    setTimeout(showSlides, 3000); // Change slide every 3 seconds
}

// Function to show a specific slide when a dot is clicked
function currentSlide(n) {
    slideIndex = n - 1; // Set the slide index to the selected slide
    showSlides(); // Call the function to update the slides
}
