from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
)


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        first_party = info.firstPartyUrl().toString()
        res_type = info.resourceType()

        if "m.youtube.com" in first_party:
            info.setHttpHeader(
                b"User-Agent",
                b"Mozilla/5.0 (Mobile; Nokia 8110 4G; rv:48.0) "
                b"Gecko/48.0 Firefox/48.0 KAIOS/2.5",
            )

            blocked_types = (
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeMedia,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeFontResource,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeWorker,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeSharedWorker,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypeServiceWorker,
                QWebEngineUrlRequestInfo.ResourceType.ResourceTypePing,
            )
            if res_type in blocked_types:
                return info.block(True)

            if res_type == QWebEngineUrlRequestInfo.ResourceType.ResourceTypeXhr:
                if "/youtubei/v1/" in url:
                    essential_api = ("next", "comment", "get_panel", "flow")
                    if not any(a in url for a in essential_api):
                        return info.block(True)
                else:
                    return info.block(True)

            blocked_substrings = (
                "googleads",
                "doubleclick",
                "log_event",
                "lottie",
                "google.com/js",
            )
            if any(p in url for p in blocked_substrings):
                return info.block(True)

            if res_type == QWebEngineUrlRequestInfo.ResourceType.ResourceTypeImage:
                if "yt3.ggpht.com" not in url and "fonts.gstatic.com" not in url:
                    info.block(True)
