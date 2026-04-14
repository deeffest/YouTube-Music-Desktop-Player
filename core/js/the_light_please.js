// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    const MEDIA = [
        "img",
        "video",
        "ytmusic-thumbnail-renderer img",
        "yt-img-shadow img",
        "[style*='background-image']",
        "ytmusic-logo",
        "yt-share-target-renderer yt-icon",
    ];

    document.head.appendChild(
        Object.assign(document.createElement("style"), {
            textContent: `
                html { filter: invert(1) hue-rotate(180deg) !important; }
                ${MEDIA.join(",")} {
                    filter: invert(1) hue-rotate(180deg) !important;
                    will-change: filter;
                }
            `,
        }),
    );
})();
