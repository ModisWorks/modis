$(function () {
    'use strict';
    var $page = $("#main");
    var target = "";
    var options = {
        debug: true,
        scroll: false,
        cacheLength: 2,
        onStart: {
            duration: 100,
            render: function ($container) {
                // Animate tabs out
                $(".page-tabs a").removeClass("page-link-current");
                // Add your CSS animation reversing class
                $container.addClass('page-out');
                // Restart your animation
                smoothState.restartCSSAnimations();

                // Scroll to top
                var $pageTabs = $(".page-tabs");
                var t = $pageTabs.offset().top + 1;
                var h = $pageTabs.offset().top + $pageTabs.height();
                if (window.scrollY > t && window.scrollY < h) {
                    $("html, body").animate({ scrollTop: t }, 150);
                }
            }
        },
        onReady: {
            duration: 0,
            render: function ($container, $newContent) {
                // Remove your CSS animation reversing class
                $container.removeClass('page-out');
                // Inject the new content
                $container.html($newContent);

                // Scroll to top
                var $pageTabs = $(".page-tabs");
                var h = $pageTabs.offset().top + $pageTabs.height() + 1;
                if (window.scrollY > h) {
                    window.scrollTo(0, h);
                }
            }
        }
    }

    var smoothState = $page.smoothState(options).data('smoothState');

    $page.on('click', ".page-tabs a", function () {
        if ($page.hasClass("page-out")) {
            $(this).addClass("page-link-current");
        }
    });
});