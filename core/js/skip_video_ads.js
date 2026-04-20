(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    const AD_SELECTORS = [
        ".ad-showing",
        ".ad-interrupting",
        ".ytp-ad-text",
        ".ytp-ad-button-icon",
        ".ytp-ad-player-overlay-flyout-cta",
        ".ytp-ad-player-overlay-flyout-cta-rounded",
    ];

    const isAdPlaying = () => {
        const player = document.querySelector("#movie_player");
        return (
            player &&
            AD_SELECTORS.some(
                (sel) => player.matches(sel) || player.querySelector(sel),
            )
        );
    };

    const skipAd = () => {
        const video = document.querySelector("video");
        if (video?.duration) video.currentTime = 9999;
    };

    new MutationObserver((mutations) => {
        for (const m of mutations) {
            for (const node of m.addedNodes) {
                if (
                    node.nodeType === 1 &&
                    AD_SELECTORS.some(
                        (sel) => node.matches(sel) || node.querySelector(sel),
                    )
                ) {
                    skipAd();
                    return;
                }
            }
        }
    }).observe(document.documentElement, { childList: true, subtree: true });

    document.addEventListener(
        "loadedmetadata",
        (e) => {
            if (e.target.tagName === "VIDEO" && isAdPlaying())
                e.target.muted = true;
        },
        true,
    );
})();
