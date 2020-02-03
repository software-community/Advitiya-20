(function ($) {
    // Galery Owl
    $('#galery-owl').owlCarousel({
        items: 1,
        loop: true,
        margin: 0,
        dots: false,
        nav: true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        autoplay: true,
        autoplaySpeed: 500,
        navSpeed: 500,
        responsive: {
            0: {
                stagePadding: 0,
            },
            768: {
                stagePadding: 120,
            }
        }
    });
})(jQuery);