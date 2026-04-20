(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    document.head.appendChild(
        Object.assign(document.createElement("style"), {
            textContent: `
                html { filter: invert(1) hue-rotate(180deg) !important; }
                img, video, ytmusic-thumbnail-renderer img, yt-img-shadow img,
                [style*='background-image'], ytmusic-logo, yt-share-target-renderer yt-icon {
                    filter: invert(1) hue-rotate(180deg) !important;
                }
            `
        })
    );
})();
