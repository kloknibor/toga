from __future__ import annotations

from typing import Callable, Protocol, Union

from toga.handlers import HandlerGeneratorReturnT, WrappedHandlerT, wrapped_handler
from toga.style import Pack
from toga.types import TypeAlias

from .base import Widget


class OnChangeHandlerSync(Protocol):
    def __call__(self, /) -> object:
        """A handler to invoke when the text input is changed."""


class OnChangeHandlerAsync(Protocol):
    async def __call__(self, /) -> object:
        """Async definition of :any:`OnChangeHandlerSync`."""


class OnChangeHandlerGenerator(Protocol):
    def __call__(self, /) -> HandlerGeneratorReturnT[object]:
        """Generator definition of :any:`OnChangeHandlerSync`."""


OnChangeHandlerT: TypeAlias = Union[
    OnChangeHandlerSync, OnChangeHandlerAsync, OnChangeHandlerGenerator
]


class OnConfirmHandlerSync(Protocol):
    def __call__(self, /) -> object:
        """A handler to invoke when the text input is confirmed."""


class OnConfirmHandlerAsync(Protocol):
    async def __call__(self, /) -> object:
        """Async definition of :any:`OnConfirmHandlerSync`."""


class OnConfirmHandlerGenerator(Protocol):
    def __call__(self, /) -> HandlerGeneratorReturnT[object]:
        """Generator definition of :any:`OnConfirmHandlerSync`."""


OnConfirmHandlerT: TypeAlias = Union[
    OnConfirmHandlerSync, OnConfirmHandlerAsync, OnConfirmHandlerGenerator
]


class OnGainFocusHandlerSync(Protocol):
    def __call__(self, /) -> object:
        """A handler to invoke when the text input gains focus."""


class OnGainFocusHandlerAsync(Protocol):
    async def __call__(self, /) -> object:
        """Async definition of :any:`OnGainFocusHandlerSync`."""


class OnGainFocusHandlerGenerator(Protocol):
    def __call__(self, /) -> HandlerGeneratorReturnT[object]:
        """Generator definition of :any:`OnGainFocusHandlerSync`."""


OnGainFocusHandlerT: TypeAlias = Union[
    OnGainFocusHandlerSync, OnGainFocusHandlerAsync, OnGainFocusHandlerGenerator
]


class OnLoseFocusHandlerSync(Protocol):
    def __call__(self, /) -> object:
        """A handler to invoke when the text input loses focus."""


class OnLoseFocusHandlerAsync(Protocol):
    async def __call__(self, /) -> object:
        """Async definition of :any:`OnLoseFocusHandlerSync`."""


class OnLoseFocusHandlerGenerator(Protocol):
    def __call__(self, /) -> HandlerGeneratorReturnT[object]:
        """Generator definition of :any:`OnLoseFocusHandlerSync`."""


OnLoseFocusHandlerT: TypeAlias = Union[
    OnLoseFocusHandlerSync, OnLoseFocusHandlerAsync, OnLoseFocusHandlerGenerator
]


class TextInput(Widget):
    """Create a new single-line text input widget."""

    def __init__(
        self,
        id: str | None = None,
        style: Pack | None = None,
        value: str | None = None,
        readonly: bool = False,
        placeholder: str | None = None,
        on_change: OnChangeHandlerT | None = None,
        on_confirm: OnConfirmHandlerT | None = None,
        on_gain_focus: OnGainFocusHandlerT | None = None,
        on_lose_focus: OnLoseFocusHandlerT | None = None,
        validators: list[Callable[[str], bool]] | None = None,
    ):
        """
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param value: The initial content to display in the widget.
        :param readonly: Can the value of the widget be modified by the user?
        :param placeholder: The content to display as a placeholder when there is no
            user content to display.
        :param on_change: A handler that will be invoked when the value of the widget
            changes.
        :param on_confirm: A handler that will be invoked when the user accepts the
            value of the input (usually by pressing Return on the keyboard).
        :param on_gain_focus: A handler that will be invoked when the widget gains
            input focus.
        :param on_lose_focus: A handler that will be invoked when the widget loses
            input focus.
        :param validators: A list of validators to run on the value of the input.
        """
        super().__init__(id=id, style=style)

        # Create a platform specific implementation of the widget
        self._create()

        self.placeholder = placeholder  # type: ignore[assignment]
        self.readonly = readonly

        # Set the actual value before on_change, because we do not want
        # on_change triggered by it However, we need to prime the handler
        # property in case it is accessed.
        self.on_change = None  # type: ignore[assignment]
        self.on_confirm = None  # type: ignore[assignment]

        # Set the list of validators before we set the initial value so that
        # validation is performed on the initial value
        self.validators = validators  # type: ignore[assignment]
        self.value = value  # type: ignore[assignment]

        self.on_change = on_change  # type: ignore[assignment]
        self.on_confirm = on_confirm  # type: ignore[assignment]
        self.on_lose_focus = on_lose_focus  # type: ignore[assignment]
        self.on_gain_focus = on_gain_focus  # type: ignore[assignment]

    def _create(self) -> None:
        self._impl = self.factory.TextInput(interface=self)

    @property
    def readonly(self) -> bool:
        """Can the value of the widget be modified by the user?

        This only controls manual changes by the user (i.e., typing at the
        keyboard). Programmatic changes are permitted while the widget has
        ``readonly`` enabled.
        """
        return self._impl.get_readonly()

    @readonly.setter
    def readonly(self, value: object) -> None:
        self._impl.set_readonly(bool(value))

    @property
    def placeholder(self) -> str:
        """The placeholder text for the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.
        """
        return self._impl.get_placeholder()

    @placeholder.setter
    def placeholder(self, value: object) -> None:
        self._impl.set_placeholder("" if value is None else str(value))
        self.refresh()

    @property
    def value(self) -> str:
        """The text to display in the widget.

        A value of ``None`` will be interpreted and returned as an empty string.
        Any other object will be converted to a string using ``str()``.

        Any newline (``\\n``) characters in the string will be replaced with a space.

        Validation will be performed as a result of changing widget value.
        """
        return self._impl.get_value()

    @value.setter
    def value(self, value: object) -> None:
        if value is None:
            v = ""
        else:
            v = str(value).replace("\n", " ")
        self._impl.set_value(v)
        self.refresh()

    @property
    def is_valid(self) -> bool:
        """Does the value of the widget currently pass all validators without error?"""
        return self._impl.is_valid()

    @property
    def on_change(self) -> WrappedHandlerT:
        """The handler to invoke when the value of the widget changes."""
        return self._on_change

    @on_change.setter
    def on_change(self, handler: OnChangeHandlerT) -> None:
        self._on_change = wrapped_handler(self, handler)

    @property
    def validators(self) -> list[Callable[[str], bool]]:
        """The list of validators being used to check input on the widget.

        Changing the list of validators will cause validation to be performed.
        """
        return self._validators

    @validators.setter
    def validators(self, validators: list[Callable[[str], bool]] | None) -> None:
        replacing = hasattr(self, "_validators")
        if validators is None:
            self._validators = []
        else:
            self._validators = validators

        if replacing:
            self._validate()

    @property
    def on_gain_focus(self) -> WrappedHandlerT:
        """The handler to invoke when the widget gains input focus."""
        return self._on_gain_focus

    @on_gain_focus.setter
    def on_gain_focus(self, handler: OnGainFocusHandlerT) -> None:
        self._on_gain_focus = wrapped_handler(self, handler)

    @property
    def on_lose_focus(self) -> WrappedHandlerT:
        """The handler to invoke when the widget loses input focus."""
        return self._on_lose_focus

    @on_lose_focus.setter
    def on_lose_focus(self, handler: OnLoseFocusHandlerT) -> None:
        self._on_lose_focus = wrapped_handler(self, handler)

    def _validate(self) -> None:
        """Validate the current value of the widget.

        If a problem is found, the widget will be put into an error state.
        """
        for validator in self.validators:
            error_message = validator(self.value)
            if error_message is not None:
                self._impl.set_error(error_message)
                break
        else:
            self._impl.clear_error()

    def _value_changed(self):
        """Validate the current value of the widget and invoke the on_change handler."""
        self._validate()
        self.on_change()

    @property
    def on_confirm(self) -> WrappedHandlerT:
        """The handler to invoke when the user accepts the value of the widget,
        usually by pressing return/enter on the keyboard.
        """
        return self._on_confirm

    @on_confirm.setter
    def on_confirm(self, handler: OnConfirmHandlerT) -> None:
        self._on_confirm = wrapped_handler(self, handler)
