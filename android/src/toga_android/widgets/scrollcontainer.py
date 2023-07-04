from travertino.size import at_least

from ..container import Container, Viewport
from ..libs.android.view import (
    Gravity,
    View__OnScrollChangeListener,
    View__OnTouchListener,
)
from ..libs.android.widget import (
    HorizontalScrollView,
    LinearLayout__LayoutParams,
    ScrollView,
)
from .base import Widget


class TogaOnTouchListener(View__OnTouchListener):
    def __init__(self):
        super().__init__()
        self.is_scrolling_enabled = True

    def onTouch(self, view, motion_event):
        if self.is_scrolling_enabled:
            return view.onTouchEvent(motion_event)
        else:
            return True


class TogaOnScrollListener(View__OnScrollChangeListener):
    def __init__(self, impl):
        super().__init__()
        self.impl = impl

    def onScrollChange(self, view, new_x, new_y, old_x, old_y):
        self.impl.interface.on_scroll(None)


class ScrollContainer(Widget, Container):
    def create(self):
        scroll_listener = TogaOnScrollListener(self)

        self.native = self.vScrollView = ScrollView(self._native_activity)
        vScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT,
        )
        vScrollView_layout_params.gravity = Gravity.TOP
        self.vScrollView.setLayoutParams(vScrollView_layout_params)
        self.vScrollListener = TogaOnTouchListener()
        self.vScrollView.setOnTouchListener(self.vScrollListener)
        self.vScrollView.setOnScrollChangeListener(scroll_listener)

        self.hScrollView = HorizontalScrollView(self._native_activity)
        hScrollView_layout_params = LinearLayout__LayoutParams(
            LinearLayout__LayoutParams.MATCH_PARENT,
            LinearLayout__LayoutParams.MATCH_PARENT,
        )
        hScrollView_layout_params.gravity = Gravity.LEFT
        self.hScrollListener = TogaOnTouchListener()
        self.hScrollView.setOnTouchListener(self.hScrollListener)
        self.hScrollView.setOnScrollChangeListener(scroll_listener)
        self.vScrollView.addView(self.hScrollView, hScrollView_layout_params)

        self.content_viewport = Viewport(self.hScrollView, self.interface)

    def set_bounds(self, x, y, width, height):
        super().set_bounds(x, y, width, height)
        self.content_viewport.size = (width, height)

    def get_vertical(self):
        return self.vScrollListener.is_scrolling_enabled

    def set_vertical(self, value):
        if not value:
            self.vScrollView.setScrollY(0)
        self.vScrollListener.is_scrolling_enabled = value

    def get_horizontal(self):
        return self.hScrollListener.is_scrolling_enabled

    def set_horizontal(self, value):
        if not value:
            self.hScrollView.setScrollX(0)
        self.hScrollListener.is_scrolling_enabled = value

    def get_vertical_position(self):
        return int(self.vScrollView.getScrollY() / self.viewport.scale)

    def get_horizontal_position(self):
        return int(self.hScrollView.getScrollX() / self.viewport.scale)

    def get_max_horizontal_position(self):
        if not self.get_horizontal():
            return 0
        else:
            return int(
                max(0, self.content_viewport.native.getWidth() - self.native.getWidth())
                / self.viewport.scale
            )

    def get_max_vertical_position(self):
        if not self.get_vertical():
            return 0
        else:
            return int(
                max(
                    0,
                    self.content_viewport.native.getHeight() - self.native.getHeight(),
                )
                / self.viewport.scale
            )

    def set_position(self, horizontal_position, vertical_position):
        self.hScrollView.setScrollX(int(horizontal_position * self.viewport.scale))
        self.vScrollView.setScrollY(int(vertical_position * self.viewport.scale))

    def set_background_color(self, value):
        self.set_background_simple(value)

    def rehint(self):
        self.interface.intrinsic.width = at_least(0)
        self.interface.intrinsic.height = at_least(0)
