(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    let previousThumbnailUrl = null;

    function getThumbnailUrl(src) {
        return src.split("?")[0];
    }

    async function cutVideo(src) {
        const player = document.querySelector(".html5-video-player");
        if (player && src && src !== previousThumbnailUrl) {
            player.style.backgroundImage = "";
            previousThumbnailUrl = null;
        }
        const url = getThumbnailUrl(src);
        if (!url) return;
        previousThumbnailUrl = src;
        Object.assign(player.style, {
            backgroundImage: `url(${url})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            backgroundRepeat: "no-repeat",
            width: "100%",
            height: "100%",
            position: "absolute",
            top: "0",
            left: "0",
        });
    }

    const thumbEl = document.querySelector(
        ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
    );
    if (thumbEl) {
        new MutationObserver((mutations) => {
            for (const m of mutations) {
                if (m.attributeName === "src") {
                    cutVideo(thumbEl.src);
                }
            }
        }).observe(thumbEl, { attributes: true });
    }
})();
