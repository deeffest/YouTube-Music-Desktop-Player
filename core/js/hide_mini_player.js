(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    const player = document.querySelector("ytmusic-player#player");
    if (!player) return;

    const toggleMiniPlayer = () => {
        const state = player.getAttribute("player-ui-state");
        player.style.display = state === "MINIPLAYER" ? "none" : "";
    };

    new MutationObserver(toggleMiniPlayer).observe(player, {
        attributes: true,
        attributeFilter: ["player-ui-state"],
    });
})();
