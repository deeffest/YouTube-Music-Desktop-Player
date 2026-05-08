(function () {
    if (window.__GM_POLYFILL_LOADED__) return;
    window.__GM_POLYFILL_LOADED__ = true;

    const PFX = "__gm__";

    const GM_addStyle = (css) => {
        const style = Object.assign(document.createElement("style"), {
            textContent: css,
        });
        (document.head || document.documentElement).appendChild(style);
        return style;
    };

    const GM_setValue = (key, value) =>
        localStorage.setItem(PFX + key, JSON.stringify(value));
    const GM_getValue = (key, def) => {
        const raw = localStorage.getItem(PFX + key);
        if (raw === null) return def;
        try {
            return JSON.parse(raw);
        } catch {
            return def;
        }
    };
    const GM_deleteValue = (key) => localStorage.removeItem(PFX + key);
    const GM_listValues = () =>
        Array.from({ length: localStorage.length }, (_, i) =>
            localStorage.key(i),
        )
            .filter((k) => k?.startsWith(PFX))
            .map((k) => k.slice(PFX.length));

    const GM_log = (...args) => console.log("[Userscript]", ...args);

    const GM_setClipboard = (data) =>
        navigator.clipboard.writeText(String(data));

    const GM_xmlhttpRequest = (details) => {
        const xhr = new XMLHttpRequest();
        xhr.open(
            (details.method || "GET").toUpperCase(),
            details.url,
            !details.synchronous,
            details.user || null,
            details.password || null,
        );
        for (const [k, v] of Object.entries(details.headers || {}))
            try {
                xhr.setRequestHeader(k, v);
            } catch {}
        if (details.overrideMimeType)
            xhr.overrideMimeType(details.overrideMimeType);
        if (details.timeout) xhr.timeout = details.timeout;
        if (details.responseType) xhr.responseType = details.responseType;

        const resp = () => ({
            readyState: xhr.readyState,
            status: xhr.status,
            statusText: xhr.statusText,
            responseText:
                typeof xhr.responseText === "string" ? xhr.responseText : "",
            responseXML: xhr.responseXML || null,
            response: xhr.response,
            responseHeaders: xhr.getAllResponseHeaders(),
            finalUrl: xhr.responseURL || details.url,
            context: details.context || null,
        });

        for (const ev of [
            "onreadystatechange",
            "onload",
            "onerror",
            "onabort",
            "ontimeout",
            "onloadstart",
            "onloadend",
        ])
            xhr[ev] = () => details[ev]?.(resp());
        xhr.onprogress = (e) =>
            details.onprogress?.({
                ...resp(),
                loaded: e.loaded,
                total: e.total,
                lengthComputable: e.lengthComputable,
            });

        if (details.upload && xhr.upload)
            for (const ev of ["onload", "onerror", "onabort", "onprogress"])
                if (typeof details.upload[ev] === "function")
                    xhr.upload[ev] = details.upload[ev];

        let body = details.data || null;
        if (details.binary && typeof body === "string") {
            const buf = new Uint8Array(body.length);
            for (let i = 0; i < body.length; i++)
                buf[i] = body.charCodeAt(i) & 0xff;
            body = buf.buffer;
        }
        xhr.send(body);
        return { abort: () => xhr.abort() };
    };

    const GM_info = {
        scriptHandler: "QtWebEngine",
        version: "1.0.0",
        scriptWillUpdate: false,
        isIncognito: false,
        platform: {
            arch: "x86-64",
            browserName: "QtWebEngine",
            browserVersion: navigator.userAgent,
            os: navigator.platform,
        },
    };

    const GM = {
        info: GM_info,
        addStyle: (css) => Promise.resolve(GM_addStyle(css)),
        setValue: (k, v) => {
            GM_setValue(k, v);
            return Promise.resolve();
        },
        getValue: (k, d) => Promise.resolve(GM_getValue(k, d)),
        deleteValue: (k) => {
            GM_deleteValue(k);
            return Promise.resolve();
        },
        listValues: () => Promise.resolve(GM_listValues()),
        setClipboard: (d) => {
            GM_setClipboard(d);
            return Promise.resolve();
        },
        xmlHttpRequest: GM_xmlhttpRequest,
    };

    Object.assign(window, {
        GM_addStyle,
        GM_setValue,
        GM_getValue,
        GM_deleteValue,
        GM_listValues,
        GM_log,
        GM_setClipboard,
        GM_xmlhttpRequest,
        GM_xmlHttpRequest: GM_xmlhttpRequest,
        GM_info,
        GM,
        unsafeWindow: window,
    });
})();
