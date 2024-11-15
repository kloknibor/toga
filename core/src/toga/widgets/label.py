from __future__ import annotations

from toga.platform import get_platform_factory

from .base import StyleT, Widget


class Label(Widget):
    def __init__(
        self,
        text: str,
        id: str | None = None,
        style: StyleT | None = None,
    ):
        """Create a new text label.

        :param text: Text of the label.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style
            will be applied to the widget.
        """
        super().__init__(id=id, style=style)

        self.text = text

    def _create(self) -> None:
        self.factory = get_platform_factory()
        self._impl = self.factory.Label(interface=self)

    def focus(self) -> None:
        """No-op; Label cannot accept input focus."""
        pass

    @property
    def text(self) -> str:
        """The text displayed by the label.

        ``None``, and the Unicode codepoint U+200B (ZERO WIDTH SPACE), will be
        interpreted and returned as an empty string. Any other object will be
        converted to a string using ``str()``.
        """
        return self._impl.get_text()

    @text.setter
    def text(self, value: object) -> None:
        if value is None or value == "\u200B":
            text = ""
        else:
            text = str(value)

        self._impl.set_text(text)
        self.refresh()
