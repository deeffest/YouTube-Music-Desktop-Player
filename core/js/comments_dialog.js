(config) => {
    if (!location.href.startsWith("https://m.youtube.com/")) return;

    const REMOVE = [
        "ytm-mobile-topbar-renderer",
        ".player-size",
        "ytm-slim-video-information-renderer",
        "ytm-slim-owner-renderer",
        "ytm-slim-video-action-bar-renderer",
        "ytm-item-section-renderer[section-identifier='related-items']",
    ];

    const setTheme = () => {
        const value = config.light_theme ? "f6=8" : "f6=400";
        if (!document.cookie.includes(value)) {
            document.cookie = `PREF=${value}; path=/; domain=.youtube.com; max-age=31536000`;
            location.reload();
        }
    };

    const injectStyles = () => {
        const style = document.createElement("style");
        style.textContent = `
            * { animation: none !important; transition: none !important; will-change: auto !important; }
            #app { overflow: hidden !important; }
            ::-webkit-scrollbar { width: 10px; height: 10px; }
            ::-webkit-scrollbar-track { background-color: transparent; }
            ::-webkit-scrollbar-corner { background-color: transparent; }
            ::-webkit-scrollbar-thumb {
                background-color: rgba(100,100,100,.6);
                border-radius: 8px;
                border: 2px solid transparent;
                background-clip: padding-box;
            }
            ::-webkit-scrollbar-thumb:hover { background-color: rgba(136,136,136,.8); }
        `;
        (document.head || document.documentElement).appendChild(style);
    };

    const cleanHead = () => {
        document
            .querySelectorAll("meta, title, script")
            .forEach((el) => el.remove());
        document.querySelectorAll("link").forEach((el) => {
            if (el.getAttribute("rel") !== "stylesheet") el.remove();
        });
    };

    const removeElements = () =>
        REMOVE.forEach((sel) =>
            document.querySelectorAll(sel).forEach((el) => el.remove()),
        );

    const expandComments = () => {
        const panel = document.querySelector(
            ".engagement-panel-section-list-background",
        );
        if (!panel) return;
        Object.assign(panel.style, {
            height: "100vh",
            minHeight: "100vh",
            position: "fixed",
            top: "0",
            left: "0",
            width: "100%",
        });
    };

    const blockLinks = (e) => {
        const href = e.target.closest("a")?.href || "";
        if (href.includes("m.youtube.com") && !href.includes(config.video_id))
            (e.preventDefault(), e.stopImmediatePropagation());
    };

    const startObserver = () => {
        new MutationObserver(() => {
            removeElements();
            expandComments();
        }).observe(document.body, { childList: true, subtree: true });
        removeElements();
        expandComments();
    };

    const startWhenReady = () => {
        if (document.body) {
            startObserver();
            return;
        }
        new MutationObserver((_, obs) => {
            if (!document.body) return;
            obs.disconnect();
            startObserver();
        }).observe(document.documentElement, { childList: true });
    };

    setTheme();
    document.addEventListener("click", blockLinks, true);
    document.addEventListener(
        "DOMContentLoaded",
        () => {
            cleanHead();
            injectStyles();
        },
        { once: true },
    );

    if (document.documentElement) {
        if (document.head) {
            cleanHead();
            injectStyles();
        }
        startWhenReady();
    } else {
        document.addEventListener(
            "DOMContentLoaded",
            () => {
                cleanHead();
                injectStyles();
                startObserver();
            },
            { once: true },
        );
    }
};
