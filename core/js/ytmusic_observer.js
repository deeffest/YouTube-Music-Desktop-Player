if (typeof qt !== "undefined" && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, (channel) => {
        const backend = channel.objects.backend;
        let lastSongState = "",
            lastSongInfo = {},
            lastSongProgress = {},
            lastLikeStatus = "";
        let debounceTimer = null,
            DEBOUNCE_DELAY = 500;

        const isAdPlaying = () =>
            !!document.querySelector(
                ".ad-showing, .ad-interrupting, .ytp-ad-text",
            );

        const getArtwork = () => {
            const src = document.querySelector(
                ".thumbnail-image-wrapper .image.style-scope.ytmusic-player-bar",
            )?.src;
            return src?.includes("lh3.googleusercontent.com")
                ? src.replace(/w\d+-h\d+/, "w544-h544")
                : src || "";
        };

        const updateSongInfo = () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const link = document.querySelector(".ytp-title-link");
                if (!link?.textContent.trim() || "") {
                    if (lastSongInfo.videoId !== "") {
                        backend.song_info_changed("", "", "", "", 0);
                        lastSongInfo = {
                            title: "",
                            artist: "",
                            artwork: "",
                            videoId: "",
                            duration: 0,
                        };
                    }
                    return;
                }

                const title =
                    document
                        .querySelector(".title.style-scope.ytmusic-player-bar")
                        ?.textContent.trim() || "";
                const artist =
                    document
                        .querySelector(".byline.style-scope.ytmusic-player-bar")
                        ?.textContent.trim()
                        .split("•")[0]
                        .trim() || "";
                const artwork = getArtwork();
                const videoId = link?.href
                    ? new URL(link.href).searchParams.get("v") || ""
                    : "";
                const duration = Math.floor(
                    document.querySelector("video")?.duration || 0,
                );

                if (!Number.isFinite(duration) || duration <= 0) return;

                const changed =
                    title !== lastSongInfo.title ||
                    artist !== lastSongInfo.artist ||
                    artwork !== lastSongInfo.artwork ||
                    videoId !== lastSongInfo.videoId;

                if (!changed || isAdPlaying()) return;

                backend.song_info_changed(
                    title,
                    artist,
                    artwork,
                    videoId,
                    duration,
                );

                lastSongInfo = {
                    title,
                    artist,
                    artwork,
                    videoId,
                    duration,
                };
            }, DEBOUNCE_DELAY);
        };

        const updateSongState = () => {
            const video = document.querySelector("video");
            const state =
                video?.readyState === 4
                    ? video.paused
                        ? "Paused"
                        : "Playing"
                    : "NoSong";
            if (state !== lastSongState) {
                if (isAdPlaying()) return;
                backend.song_state_changed(state);
                lastSongState = state;
            }
        };

        const updateSongProgress = () => {
            const [currentTime, totalTime] =
                document
                    .querySelector(".time-info.style-scope.ytmusic-player-bar")
                    ?.textContent.trim()
                    .split("/")
                    .map((t) => t.trim()) || [];
            if (
                currentTime !== lastSongProgress.currentTime ||
                totalTime !== lastSongProgress.totalTime
            ) {
                if (isAdPlaying()) return;
                backend.song_progress_changed(currentTime, totalTime);
                lastSongProgress = { currentTime, totalTime };
            }
        };

        const updateSongStatus = () => {
            const likeButton = document.querySelector("#like-button-renderer");
            if (!likeButton) return;

            let likeStatus = likeButton.getAttribute("like-status");
            if (!likeStatus || likeStatus === lastLikeStatus) return;

            likeStatus =
                likeStatus.charAt(0).toUpperCase() +
                likeStatus.slice(1).toLowerCase();

            if (isAdPlaying()) return;
            backend.song_status_changed(likeStatus);
            lastLikeStatus = likeStatus;
        };

        const observe = (el, fn, opts) =>
            el && new MutationObserver(fn).observe(el, opts);

        observe(
            document.querySelector(
                ".middle-controls.style-scope.ytmusic-player-bar",
            ),
            updateSongInfo,
            { childList: true, subtree: true },
        );
        observe(document.querySelector("ytmusic-player"), updateSongState, {
            childList: true,
            subtree: true,
        });
        observe(
            document.querySelector(".time-info.style-scope.ytmusic-player-bar"),
            updateSongProgress,
            { characterData: true, subtree: true },
        );
        observe(
            document.querySelector(
                "ytmusic-player-bar ytmusic-like-button-renderer#like-button-renderer",
            ),
            updateSongStatus,
            { attributes: true, attributeFilter: ["like-status"] },
        );

        const addVideoListeners = () => {
            const video = document.querySelector("video");
            if (!video || video._ytBound) return;

            video._ytBound = true;
            video.addEventListener("loadedmetadata", updateSongInfo);
            video.addEventListener("durationchange", updateSongInfo);
        };

        addVideoListeners();
        observe(document.body, addVideoListeners, {
            childList: true,
            subtree: true,
        });

        updateSongInfo();
        updateSongState();
        updateSongProgress();
        updateSongStatus();
    });
}
