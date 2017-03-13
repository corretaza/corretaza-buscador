
/***************** Slide-In Nav ******************/

$(window).load(function() {

	$('.nav_slide_button').click(function() {
		$('.pull').slideToggle();
	});

});

/***************** Smooth Scrolling ******************/

$(function() {

	$('a[href*=#]:not([href=#])').click(function() {
		if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {

			var target = $(this.hash);
			target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
			if (target.length) {
				$('html,body').animate({
					scrollTop: target.offset().top
				}, 2000);
				return false;
			}
		}
	});

});

/***************** Nav Transformicon ******************/

//document.querySelector("#nav-toggle").addEventListener("click", function() {
//	this.classList.toggle("active");
//});

/***************** Overlays ******************/

$(document).ready(function(){
    if (Modernizr.touch) {
        // show the close overlay button
        $(".close-overlay").removeClass("hidden");
        // handle the adding of hover class when clicked
        $(".img").click(function(e){
            if (!$(this).hasClass("hover")) {
                $(this).addClass("hover");
            }
        });
        // handle the closing of the overlay
        $(".close-overlay").click(function(e){
            e.preventDefault();
            e.stopPropagation();
            if ($(this).closest(".img").hasClass("hover")) {
                $(this).closest(".img").removeClass("hover");
            }
        });
    } else {
        // handle the mouseenter functionality
        $(".img").mouseenter(function(){
            $(this).addClass("hover");
        })
        // handle the mouseleave functionality
        .mouseleave(function(){
            $(this).removeClass("hover");
        });
    }
});


/*** infinite scroll (ajax pagination) ***/
$(function(){
    var grid = $('#paginationGrid');

    // all attrs are $jquery selectors, so you can use "#value" or ".value" in data-props
    var selector = grid.attr('data-pag-selector');
    var nextSelector = grid.attr('data-pag-next');
    var itemSelector = grid.attr('data-item-selector');

    grid.infinitescroll({
        navSelector: selector,
        nextSelector: nextSelector,
        itemSelector: itemSelector,
        loadingText: 'Carregando mais resultados...',
        donetext: ''
    },

    function(new_elts) {
        var elts = $(new_elts).css('opacity', 0);
        elts.animate({opacity: 1});

        grid.append(elts);
    });
});

