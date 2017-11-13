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
                var $mainContent = $(".main-content");
                var t = $mainContent.offset().top + 1;
                if (window.scrollY > t) {
                    window.scrollTo(0, t);
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

    // Update tab bar
    updateTabs();
    window.onscroll = updateTabs;
});

function updateTabs() {
    var $mainContent = $(".main-content");
    var $pageTabs = $("#PageTabs");

    var t = $mainContent.offset().top + 1;
    if (window.scrollY > t) {
        if (!$pageTabs.hasClass("fixed")) {
            $pageTabs.addClass("fixed")
        }
    } else {
        if ($pageTabs.hasClass("fixed")) {
            $pageTabs.removeClass("fixed")
        }
    }
}