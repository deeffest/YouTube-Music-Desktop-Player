// ==UserScript==
// @match        https://music.youtube.com/*
// ==/UserScript==

(function () {
    const container = document.querySelector("ytmusic-popup-container");
    if (!container) return;

    let video = null;
    let wasPlaying = false;

    new MutationObserver(() => {
        if (video) return;
        video = document.querySelector("video");
        if (!video) return;
        video.addEventListener("play", () => (wasPlaying = true));
        video.addEventListener("pause", () => (wasPlaying = false));
    }).observe(document.documentElement, { childList: true, subtree: true });

    new MutationObserver((mutations) => {
        for (const { type, attributeName, target, oldValue } of mutations) {
            if (
                type === "attributes" &&
                attributeName === "class" &&
                target.classList.contains("paper-toast-open") &&
                !oldValue?.includes("paper-toast-open") &&
                target.querySelector("#action-button") &&
                !target.querySelector("#action-button button[aria-disabled]")
            ) {
                target.style.display = "none";
                if (wasPlaying) video?.play();
                return;
            }
        }
    }).observe(container, {
        subtree: true,
        attributes: true,
        attributeFilter: ["class"],
        attributeOldValue: true,
    });
})();
