from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QAction

    class MultiAction(QAction): ...  # noqa: E701

else:

    class MultiAction:
        def __init__(self):
            self._actions = []

        def add(self, menu, action):
            menu.addAction(action)
            self._actions.append(action)

        def __getattr__(self, name):
            if not self._actions:
                raise AttributeError(f"No actions, cannot call '{name}'")
            attr = getattr(self._actions[0], name)
            if callable(attr):

                def method(*args, **kwargs):
                    results = [getattr(a, name)(*args, **kwargs) for a in self._actions]
                    return results[0]

                return method
            return attr
