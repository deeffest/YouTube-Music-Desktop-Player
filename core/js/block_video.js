(function () {
    if (!location.href.startsWith("https://music.youtube.com/")) return;

    const origAddSourceBuffer = MediaSource.prototype.addSourceBuffer;
    MediaSource.prototype.addSourceBuffer = function (mime) {
        if (!mime.includes("video"))
            return origAddSourceBuffer.call(this, mime);

        return {
            appendBuffer() {
                this.updating = false;
                this._updateEnd();
            },
            remove() {},
            abort() {},
            updating: false,
            buffered: {
                length: 1,
                start: () => 0,
                end: () => document.querySelector("video")?.duration || 43200,
            },
            addEventListener() {},
            removeEventListener() {},
            dispatchEvent() {
                return false;
            },
            _updateEnd() {
                this.dispatchEvent(new Event("updateend"));
            },
        };
    };

    const origXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (method, url) {
        if (url.includes("mime=video")) return this.abort();
        return origXHROpen.apply(this, arguments);
    };

    const origFetch = window.fetch;
    window.fetch = (...args) => {
        const url = typeof args[0] === "string" ? args[0] : args[0]?.url || "";
        if (url.includes("mime=video"))
            return Promise.resolve(new Response(null, { status: 204 }));
        return origFetch.apply(this, args);
    };
})();
