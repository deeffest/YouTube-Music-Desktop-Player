from PySide6.QtWebEngineCore import (
    QWebEngineUrlRequestInterceptor,
    QWebEngineUrlRequestInfo,
)


class WebEngineUrlRequestInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        first_party = info.firstPartyUrl().toString()
        res_type = info.resourceType()
        RT = QWebEngineUrlRequestInfo.ResourceType

        if "m.youtube.com" in first_party:
            info.setHttpHeader(
                b"User-Agent",
                b"Mozilla/5.0 (Mobile; Nokia 8110 4G; rv:48.0) "
                b"Gecko/48.0 Firefox/48.0 KAIOS/2.5",
            )

            strictly_blocked = (
                RT.ResourceTypeMedia,
                RT.ResourceTypeFontResource,
                RT.ResourceTypeWorker,
                RT.ResourceTypeSharedWorker,
                RT.ResourceTypeServiceWorker,
                RT.ResourceTypePing,
            )
            if res_type in strictly_blocked:
                return info.block(True)

            if res_type == RT.ResourceTypeXhr:
                if "/youtubei/v1/" in url:
                    essential_api = ("next", "comment", "get_panel", "flow")
                    if not any(a in url for a in essential_api):
                        return info.block(True)
                else:
                    return info.block(True)

            patterns = (
                "googleads",
                "doubleclick",
                "log_event",
                "lottie",
                "google.com/js",
            )
            if any(p in url for p in patterns):
                return info.block(True)

            if res_type == RT.ResourceTypeImage:
                if "yt3.ggpht.com" not in url and "fonts.gstatic.com" not in url:
                    info.block(True)
