$(document).ready(function () {
    $(".videoBlock").on("wheel", function (event) {
        event.preventDefault();
        
        let scrollAmount = event.originalEvent.deltaY || event.originalEvent.deltaX; 
        $(this).stop().animate({
            scrollLeft: "+=" + scrollAmount
        }, 200); // Smooth Scrolling
    });

    $("#commentsScroll").on("scroll", function (event) {
        event.preventDefault();
        
        let scrollAmount = event.originalEvent.deltaY || event.originalEvent.deltaX; 
    });

    $("select[name='sort']").on("change", function() {
        var sortValue = $(this).val();  
        var categorySlug = $(this).closest(".category-section").data("category-slug"); // Get the category slug from the closest parent element
        var sortUrl = $(this).data("url");
        var videoBlock = $(this).closest(".category-section").find("#videoBlock"+categorySlug);

        $.ajax({
            url: sortUrl,
            type: "GET",
            data: {
                category: categorySlug,
                sort: sortValue
            },
            dataType: "json",
            success: function(response) {
                if (response.videos && response.videos.length > 0) {
                    videoBlock.empty();

                    $.each(response.videos, function(index, v) {
                        var videoHTML = `
                            <div class="videoThumbnail">
                                <a href="/${v.category_slug}/${v.slug}/"><img src="${v.thumbnail}" alt="" style="width:100%"></a>
                                <h3>${v.title}</h3>
                                <div class="videoInfo">
                                    <p class="creator">${v.username}</p>
                                    <p class="published">${v.created}</p>
                                    <p class="dislikes">Dislikes: ${v.dislikes}</p>
                                    <p class="views">Views: ${v.views}</p>
                                </div>
                            </div>`;
                        videoBlock.append(videoHTML);
                    });
                } else {
                    videoBlock.html("<p>No videos found.</p>");
                }
            }
        });
    });
});