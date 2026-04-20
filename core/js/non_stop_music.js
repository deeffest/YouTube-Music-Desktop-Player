(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    const isDialogActive = (d) =>
        d?.closest("tp-yt-paper-dialog") &&
        !d.closest("tp-yt-paper-dialog").hasAttribute("aria-hidden");

    const autoResume = () => {
        const dialog = document.querySelector("ytmusic-you-there-renderer");
        if (!isDialogActive(dialog)) return;

        dialog.querySelector("yt-button-renderer")?.click();
        document.querySelector("video")?.play();
    };

    new MutationObserver(autoResume).observe(
        document.querySelector("ytmusic-popup-container"),
        { childList: true, subtree: true },
    );
})();
