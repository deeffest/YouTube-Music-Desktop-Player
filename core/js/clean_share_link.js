(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    const cleanUrl = (url) => {
        const u = new URL(url);
        u.searchParams.delete("si");
        return u.toString();
    };

    const descriptor = Object.getOwnPropertyDescriptor(
        HTMLInputElement.prototype,
        "value",
    );
    Object.defineProperty(HTMLInputElement.prototype, "value", {
        get: descriptor.get,
        set(val) {
            descriptor.set.call(
                this,
                this.id === "share-url" ? cleanUrl(String(val)) : val,
            );
        },
    });

    new MutationObserver(() => {
        const input = document.querySelector(
            "yt-copy-link-renderer #share-url",
        );
        if (input?.value?.includes("si="))
            descriptor.set.call(input, cleanUrl(input.value));
    }).observe(document.querySelector("ytmusic-popup-container"), {
        childList: true,
        subtree: true,
    });
})();
