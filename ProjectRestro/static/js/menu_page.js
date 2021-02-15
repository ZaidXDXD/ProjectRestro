// Trigger event on tab click
$('[dd-sidebar-tab]').on('click', function() {
	$('.sidebar-list-menu-active-bar').css('margin-top', ( $(this).attr('dd-active-tab') - 1) * $(this).height());
	$('.sidebar-list-menu li a').removeClass('active');
	$(this).addClass('active');
	$('html, body').animate({
        scrollTop: $("#content_"+$(this).attr('dd-active-tab')).offset().top
    }, 500);
});


// SCroll event
$(window).scroll(function(event) {
	var scrollPos = $(document).scrollTop();
    $('.sidebar-list-menu li a').each(function () {
        var currLink = $(this);
        var refElement = $(currLink.attr("href"));
        if (refElement.position().top <= scrollPos && refElement.position().top + refElement.height() > scrollPos) {
    		$('.sidebar-list-menu li a').removeClass("active");
        	currLink.addClass('active');
            $('.sidebar-list-menu-active-bar').css('margin-top', ( currLink.attr('dd-active-tab') - 1) * currLink.height() );
        }
    });
});