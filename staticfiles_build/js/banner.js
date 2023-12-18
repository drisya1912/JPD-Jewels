const carousel = document.querySelector(".carousel");
const prevButton = document.querySelector(".prev-button");
const nextButton = document.querySelector(".next-button");
let currentIndex = 0;

nextButton.addEventListener("click", () => {
    if (currentIndex < carousel.children.length - 1) {
        currentIndex++;
    } else {
        currentIndex = 0;
    }
    updateCarousel();
});

prevButton.addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex--;
    } else {
        currentIndex = carousel.children.length - 1;
    }
    updateCarousel();
});

function updateCarousel() {
    const translateX = -currentIndex * 100;
    carousel.style.transform = `translateX(${translateX}%)`;
}

// Optional: Automatically advance the carousel
setInterval(() => {
    nextButton.click();
}, 5000); // Change slides every 5 seconds (adjust as needed)
