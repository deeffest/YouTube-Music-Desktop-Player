import os
import ctypes
from ctypes import wintypes, byref

from comtypes.client import CreateObject
from comtypes import GUID, COMMETHOD, HRESULT, IUnknown

THB_ICON = 0x0002
THB_TOOLTIP = 0x0004
THB_FLAGS = 0x0008

THBF_ENABLED = 0x0000
THBF_DISABLED = 0x0001
THBF_NOBACKGROUND = 0x0002
THBF_HIDDEN = 0x0004
THBF_NONINTERACTIVE = 0x0008

WM_COMMAND = 0x0111
THBN_CLICKED = 0x1800


class THUMBBUTTON(ctypes.Structure):
    _fields_ = [
        ("dwMask", ctypes.c_uint),
        ("iId", ctypes.c_uint),
        ("iBitmap", ctypes.c_uint),
        ("hIcon", ctypes.c_void_p),
        ("szTip", ctypes.c_wchar * 260),
        ("dwFlags", ctypes.c_uint),
    ]


class ITaskbarList3(IUnknown):
    _iid_ = GUID("{EA1AFB91-9E28-4B86-90E9-9E9F8A5EEFAF}")
    _methods_ = [
        COMMETHOD([], HRESULT, "HrInit"),
        COMMETHOD([], HRESULT, "AddTab", (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "DeleteTab", (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "ActivateTab", (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD([], HRESULT, "SetActiveAlt", (["in"], wintypes.HWND, "hwnd")),
        COMMETHOD(
            [],
            HRESULT,
            "MarkFullscreenWindow",
            (["in"], wintypes.HWND, "hwnd"),
            (["in"], wintypes.BOOL, "fullscreen"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetProgressValue",
            (["in"], wintypes.HWND, "hwnd"),
            (["in"], ctypes.c_ulonglong, "completed"),
            (["in"], ctypes.c_ulonglong, "total"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetProgressState",
            (["in"], wintypes.HWND, "hwnd"),
            (["in"], wintypes.DWORD, "flags"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "RegisterTab",
            (["in"], wintypes.HWND, "tab"),
            (["in"], wintypes.HWND, "mdi"),
        ),
        COMMETHOD([], HRESULT, "UnregisterTab", (["in"], wintypes.HWND, "tab")),
        COMMETHOD(
            [],
            HRESULT,
            "SetTabOrder",
            (["in"], wintypes.HWND, "tab"),
            (["in"], wintypes.HWND, "insert_before"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "SetTabActive",
            (["in"], wintypes.HWND, "tab"),
            (["in"], wintypes.HWND, "mdi"),
            (["in"], wintypes.DWORD, "flags"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ThumbBarAddButtons",
            (["in"], wintypes.HWND, "hwnd"),
            (["in"], wintypes.UINT, "count"),
            (["in"], ctypes.POINTER(THUMBBUTTON), "buttons"),
        ),
        COMMETHOD(
            [],
            HRESULT,
            "ThumbBarUpdateButtons",
            (["in"], wintypes.HWND, "hwnd"),
            (["in"], wintypes.UINT, "count"),
            (["in"], ctypes.POINTER(THUMBBUTTON), "buttons"),
        ),
    ]


CLSID_TaskbarList = GUID("{56FDF344-FD6D-11d0-958A-006097C9A090}")


class _GdiStartup(ctypes.Structure):
    _fields_ = [("GdiplusVersion", ctypes.c_uint)]


_gdi = ctypes.windll.gdiplus
_gdi_token = ctypes.c_ulong()
_gdi.GdiplusStartup(byref(_gdi_token), byref(_GdiStartup(1)), None)


def _load_icon(path):
    if not path:
        return 0
    bmp, ico = ctypes.c_void_p(), ctypes.c_void_p()
    _gdi.GdipCreateBitmapFromFile(ctypes.c_wchar_p(os.path.abspath(path)), byref(bmp))
    _gdi.GdipCreateHICONFromBitmap(bmp, byref(ico))
    _gdi.GdipDisposeImage(bmp)
    return ico.value


class TaskbarAPI:
    def __init__(self):
        self._taskbar = CreateObject(CLSID_TaskbarList, interface=ITaskbarList3)
        self._hwnd = None
        self._msg_created = ctypes.windll.user32.RegisterWindowMessageW(
            "TaskbarButtonCreated"
        )
        self._buttons = {}

    def register(self, hwnd):
        self._hwnd = hwnd
        self._taskbar.HrInit()
        self._taskbar.SetProgressState(hwnd, 0)

    def add_buttons(self, buttons):
        if not self._hwnd:
            return
        btn_array = (THUMBBUTTON * len(buttons))()
        for i, btn in enumerate(buttons):
            bid = btn.get("id")
            icon_path = btn.get("icon")
            tooltip = btn.get("tooltip", "")
            flags = btn.get("flags", THBF_ENABLED)

            hicon = _load_icon(icon_path)
            self._buttons[bid] = {"hIcon": hicon, "tooltip": tooltip, "flags": flags}

            btn_array[i].dwMask = THB_ICON | THB_TOOLTIP | THB_FLAGS
            btn_array[i].iId = bid
            btn_array[i].hIcon = hicon
            btn_array[i].szTip = tooltip
            btn_array[i].dwFlags = flags

        self._taskbar.ThumbBarAddButtons(self._hwnd, len(buttons), btn_array)

    def update_button(self, button_id, icon=None, tooltip=None, flags=None):
        if not self._hwnd or button_id not in self._buttons:
            return

        data = self._buttons[button_id]
        mask = 0

        if icon is not None:
            old = data.get("hIcon")
            if old:
                ctypes.windll.user32.DestroyIcon(old)
            data["hIcon"] = _load_icon(icon)
            mask |= THB_ICON

        if tooltip is not None:
            data["tooltip"] = tooltip
            mask |= THB_TOOLTIP

        if flags is not None:
            data["flags"] = flags
            mask |= THB_FLAGS

        if mask == 0:
            return

        btn = THUMBBUTTON()
        btn.iId = button_id
        btn.dwMask = mask
        btn.hIcon = data["hIcon"]
        btn.szTip = data["tooltip"]
        btn.dwFlags = data["flags"]

        self._taskbar.ThumbBarUpdateButtons(self._hwnd, 1, (THUMBBUTTON * 1)(btn))

    def handle_message(self, msg_ptr):
        msg = wintypes.MSG.from_address(msg_ptr)
        if msg.message == self._msg_created:
            return {"type": "created"}
        if msg.message == WM_COMMAND and (msg.wParam >> 16) & 0xFFFF == THBN_CLICKED:
            return {"type": "click", "id": msg.wParam & 0xFFFF}
        return None
