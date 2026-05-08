(function() {
    if (!window.trustedTypes || !window.trustedTypes.createPolicy) return;
    try {
        window.trustedTypes.createPolicy('default', {
            createHTML:      s => s,
            createScript:    s => s,
            createScriptURL: s => s,
        });
    } catch (e) {}
})();
