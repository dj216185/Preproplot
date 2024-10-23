document.addEventListener('DOMContentLoaded', function () {
    const imageContainer = document.querySelector('.image-container');
    const images = document.querySelectorAll('.slider-image');
    let currentIndex = 0;

    function loopImages() {
        currentIndex++;
        if (currentIndex >= images.length) {
            currentIndex = 0;
            imageContainer.appendChild(images[0]);  // Move the first image to the end
            images[0].style.transform = '';  // Reset the transform
        }
        imageContainer.style.transform = `translateX(-${100 * currentIndex}%)`;

        // Move the first image to the end if it goes out of view
        if (currentIndex === images.length - 1) {
            setTimeout(() => {
                imageContainer.appendChild(images[0]);
                imageContainer.style.transition = 'none';
                imageContainer.style.transform = 'translateX(0)';
                setTimeout(() => {
                    imageContainer.style.transition = 'transform 0.5s ease-in-out';
                });
            }, 500);  // Wait for the transition to finish
        }
    }

    setInterval(loopImages, 3000);  // Change images every 3 seconds
});
