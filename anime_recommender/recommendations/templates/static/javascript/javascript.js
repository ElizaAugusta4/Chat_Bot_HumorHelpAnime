$(document).ready(function() {
    const carousel = $(".carousel");
    const prevBtn = $(".prev-btn");
    const nextBtn = $(".next-btn");
    const cardWidth = $(".anime-card").outerWidth(true);

    let currentTranslate = 0;

    nextBtn.click(function() {
        currentTranslate -= cardWidth;
        carousel.css("transform", `translateX(${currentTranslate}px)`);
    });

    prevBtn.click(function() {
        currentTranslate += cardWidth;
        carousel.css("transform", `translateX(${currentTranslate}px)`);
    });
});