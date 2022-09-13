
from typing import Dict, List, Union, Callable

from . import HTML

from .bootstrap_HTML_container import *
from js import bootstrap  # type: ignore

class Div(BootstrapContainer):
    pass
class Button(HTML.Button, BootstrapContainer):
    _default_class_name = "btn"

    def make_large(self):
        self.remove_class("btn-sm")
        self.add_class("btn-lg")

    def make_small(self):
        self.remove_class("btn-lg")
        self.add_class("btn-sm")

    def make_collapse_toggle(self, target_element: HTML.Element):
        self.set_attribute("data-bs-toggle", "collapse")
        self.set_attribute("data-bs-target", f"#{target_element.id}")

    @property
    def is_toggle_button(self) -> bool:
        return self.has_attribute("data-bs-toggle")

    @is_toggle_button.setter
    def is_toggle_button(self, value: bool):
        if value:
            self.set_attribute("data-bs-toggle", "button")
            self.set_attribute("autocomplete", "off")
        else:
            self.remove_attribute("data-bs-toggle")
            self.remove_attribute("autocomplete")

    @property
    def is_toggle_button_active(self) -> Union[bool, None]:
        """
        returns the current state of the toggle button. If this is not a toggle button, returns None
        (use is_toggle_button to control whether this is a toggle button)
        """
        if not self.is_toggle_button:
            return None
        return self.has_class("active")

    @is_toggle_button_active.setter
    def is_toggle_button_active(self, value: bool):
        if not self.is_toggle_button:
            raise ValueError("This is not a toggle button")
        if value:
            self.add_class("active")
            self.set_attribute("aria-pressed", True)
        else:
            self.remove_class("active")
            self.set_attribute("aria-pressed", False)

    def toggle(self):
        self.is_toggle_button_active = not self.is_toggle_button_active

# Accordion: ------------------------------------------------------------------


class AccordionHeader(HTML.H2, BootstrapContainer):

    _default_class_name: str = "accordion-header"


class AccordionBody(BootstrapContainer):

    _default_class_name: str = "accordion-body"


class AccordionItem(BootstrapContainer):

    _default_class_name: str = "accordion-item"

    def __init__(self,
                 content: Union[str, HTML.Element],
                 header_title: str,
                 show_on_default: bool = False,
                 stay_open: bool = False,
                 id=None,
                 class_name=None,
                 parent=None,
                 inner_html=None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        header = AccordionHeader()

        button = Button(class_name="accordion-button",
                        inner_html=header_title, parent=header)
        collapsable_body_container = BootstrapContainer(
            class_name="accordion-collapse collapse")
        if show_on_default:
            collapsable_body_container.add_class("show")
        else:
            button.add_class("collapsed")
        if not stay_open:
            collapsable_body_container.set_attribute(
                "data-bs-parent", f"#{parent.id}")
        body = AccordionBody(parent=collapsable_body_container)

        if isinstance(content, str):
            body.inner_html = content
        else:
            body.append_child(content)

        button.make_collapse_toggle(collapsable_body_container)

        self._header = header
        self._body = body

        self.append_child(header)
        self.append_child(collapsable_body_container)

    @property
    def header(self) -> AccordionHeader:
        return self._header

    @property
    def body(self) -> AccordionBody:
        return self._body


class Accordion(BootstrapContainer):

    _default_class_name: str = "accordion"

    def add_accordion_item(self,
                           content: Union[str, HTML.Element],
                           header_title: str,
                           show_on_default: bool = False,
                           stay_open: bool = False) -> None:
        return AccordionItem(content=content,
                             header_title=header_title,
                             parent=self,
                             show_on_default=show_on_default,
                             stay_open=stay_open)


class AccordionFlush(Accordion):

    _default_class_name: str = "accordion-flush"

# Alerts: ---------------------------------------------------------------------


class Alert(BootstrapContainer):

    _default_class_name: str = "alert"

    def __init__(self,
                 content: Union[str, HTML.Element],
                 show_close_button: bool = True,
                 fade: bool = True,
                 id=None,
                 class_name=None,
                 parent=None,
                 inner_html=None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if isinstance(content, str):
            self.inner_html = content
        else:
            self.append_child(content)

        self.set_attribute("role", "alert")

        if fade:
            self.add_class("fade")

        if show_close_button:
            self.add_classes("alert-dismissible", "show")
            close_btn = Button(class_name="btn-close")
            close_btn.set_attribute("data-bs-dismiss", "alert")
            close_btn.set_attribute("aria-label", "Close")
            self.append_child(close_btn)


class AlertPrimary(Alert):

    _default_class_name: str = "alert alert-primary"


class AlertSecondary(Alert):

    _default_class_name: str = "alert alert-secondary"


class AlertSuccess(Alert):

    _default_class_name: str = "alert alert-success"


class AlertDanger(Alert):

    _default_class_name: str = "alert alert-danger"


class AlertWarning(Alert):

    _default_class_name: str = "alert alert-warning"


class AlertInfo(Alert):

    _default_class_name: str = "alert alert-info"


class AlertLight(Alert):

    _default_class_name: str = "alert alert-light"


class AlertDark(Alert):

    _default_class_name: str = "alert alert-dark"

# Badges: ---------------------------------------------------------------------


class Badge(HTML.Span, BootstrapContainer):

    _default_class_name: str = "badge"

    def __init__(self,
                 content: Union[str, HTML.Element],
                 pill: bool = False,
                 id=None,
                 class_name=None,
                 parent=None,
                 inner_html=None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if isinstance(content, str):
            self.inner_html = content
        else:
            self.append_child(content)

        if pill:
            self.add_class("rounded-pill")


class BadgePrimary(Badge):

    _default_class_name: str = "badge bg-primary"


class BadgeSecondary(Badge):

    _default_class_name: str = "badge bg-secondary"


class BadgeSuccess(Badge):

    _default_class_name: str = "badge bg-success"


class BadgeDanger(Badge):

    _default_class_name: str = "badge bg-danger"


class BadgeWarning(Badge):

    _default_class_name: str = "badge bg-warning"


class BadgeInfo(Badge):

    _default_class_name: str = "badge bg-info"


class BadgeLight(Badge):

    _default_class_name: str = "badge bg-light"


class BadgeDark(Badge):

    _default_class_name: str = "badge bg-dark"

# Breadcrumb: -----------------------------------------------------------------


class Breadcrumb(HTML.Nav, BootstrapContainer):

    _default_class_name: str = "breadcrumb"

    def __init__(self,
                 id=None,
                 class_name=None,
                 parent=None,
                 path: List[str] = None,
                 links: List[Union[str, None]] = None,
                 custom_divider: str = None,
                 inner_html=None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        self.set_attribute("aria-label", "breadcrumb")

        if custom_divider is not None:
            self.element.style = f"--bs-breadcrumb-divider: '{custom_divider}';"

        self._ordered_list = None
        self._paths = []
        self._links = []

        if path is not None and links is not None:
            self.set_path(path, links)

    def _add_breadcrumb_item(self, path_part, link, is_active: bool = False) -> None:
        li = HTML.Li(parent=self._ordered_list, class_name="breadcrumb-item")
        if is_active:
            li.add_class("active")
            li.set_attribute("aria-current", "page")
        if link is not None:
            li.append_child(HTML.A(href=link, inner_html=path_part))
        else:
            li.inner_html = path_part
        return li

    def _update_path(self):
        if self._ordered_list is not None:
            self._ordered_list.destroy()
        self._ordered_list = HTML.Ol(parent=self)

        n = len(self._paths)
        for i, (part, link) in enumerate(zip(self._paths, self._links)):
            self._add_breadcrumb_item(part, link, is_active=i == n-1)

    def set_path(self, path: List[str], links: List[str] = None) -> None:
        if links is None:
            links = [None] * len(path)

        self._paths = path
        self._links = links

        self._update_path()

    @property
    def path(self) -> List[str]:
        return self._paths

    @property
    def links(self) -> List[str]:
        return self._links


# Buttons:---------------------------------------------------------------------


class ButtonPrimary(Button, BootstrapContainer):
    _default_class_name = "btn btn-primary"


class ButtonSecondary(Button):
    _default_class_name = "btn btn-secondary"


class ButtonSuccess(Button):
    _default_class_name = "btn btn-success"


class ButtonDanger(Button):
    _default_class_name = "btn btn-danger"


class ButtonWarning(Button):
    _default_class_name = "btn btn-warning"


class ButtonInfo(Button):
    _default_class_name = "btn btn-info"


class ButtonLight(Button):
    _default_class_name = "btn btn-light"


class ButtonDark(Button):
    _default_class_name = "btn btn-dark"


class ButtonLink(Button):
    _default_class_name = "btn btn-link"


class ButtonOutlinePrimary(Button):
    _default_class_name = "btn btn-outline-primary"


class ButtonOutlineSecondary(Button):
    _default_class_name = "btn btn-outline-secondary"


class ButtonOutlineSuccess(Button):
    _default_class_name = "btn btn-outline-success"


class ButtonOutlineDanger(Button):
    _default_class_name = "btn btn-outline-danger"


class ButtonOutlineWarning(Button):
    _default_class_name = "btn btn-outline-warning"


class ButtonOutlineInfo(Button):
    _default_class_name = "btn btn-outline-info"


class ButtonOutlineLight(Button):
    _default_class_name = "btn btn-outline-light"


class ButtonOutlineDark(Button):
    _default_class_name = "btn btn-outline-dark"


class ButtonClose(Button):
    _default_class_name = "btn btn-close"


class ButtonCloseWhite(ButtonClose):
    _default_class_name = "btn btn-close-white"

# Button Groups:---------------------------------------------------------------


class ButtonGroup(BootstrapContainer):
    _default_class_name = "btn-group"

    def add_button(self, button: Button):
        self.append_child(button)


class ButtonGroupVertical(ButtonGroup):
    _default_class_name = "btn-group-vertical"


class ButtonGroupToolbar(ButtonGroup):
    _default_class_name = "btn-toolbar"


class ButtonHamburger(Button):

    _default_class_name: str = "navbar-toggler"

    def __init__(self, inner_html: str = None, id: str = None, class_name: str = None, parent: HTML.Element = None, type: str = "button", name: str = None, value: str = None, onclick=None) -> None:
        super().__init__(inner_html=inner_html, id=id, class_name=class_name,
                         parent=parent, type=type, name=name, value=value, onclick=onclick)

        HTML.Span(parent=self, class_name="navbar-toggler-icon")

# Bootstrap Media: ------------------------------------------------------------


class Image(HTML.Image, BootstrapContainer):
    _default_class_name = "img-responsive"


class Video(HTML.Video, BootstrapContainer):
    _default_class_name = "img-responsive"


class ImageFluid(Image):
    _default_class_name = "img-fluid"


class Thumbnail(Image):
    _default_class_name = "img-thumbnail"


# Cards:-----------------------------------------------------------------------


class Card(BootstrapContainer):
    _default_class_name = "card"

    def __init__(self, card_body: HTML.Div,
                 title_image: Image = None,
                 card_header: HTML.Div = None,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None) -> None:

        super().__init__(inner_html, id, class_name, parent)

        if card_body is not None:
            card_body.add_class("card-body")

        if title_image is not None:
            title_image.add_class("card-img-top")

        if card_header is not None:
            card_header.class_name = "card-header"

        self._card_body = card_body
        self._title_image = title_image
        self._card_header = card_header

        self.append_child(card_body)
        self.append_child(title_image)
        self.append_child(card_header)

    @property
    def card_body(self) -> HTML.Div:
        return self._card_body

    @card_body.setter
    def card_body(self, card_body: HTML.Div) -> None:
        card_body.class_name = "card-body"
        if self._card_body is not None:
            self._card_body.destroy()
        self._card_body = card_body
        self.append_child(card_body)

    @property
    def title_image(self) -> HTML.Image:
        return self._title_image

    @title_image.setter
    def title_image(self, title_image: HTML.Image) -> None:
        title_image.class_name = "card-img-top"
        if self._title_image is not None:
            self._title_image.destroy()
        self._title_image = title_image
        self.append_child(title_image)

    @property
    def card_header(self) -> HTML.Div:
        return self._card_header

    @card_header.setter
    def card_header(self, card_header: HTML.Div) -> None:
        card_header.class_name = "card-header"
        if self._card_header is not None:
            self._card_header.destroy()
        self._card_header = card_header
        self.append_child(card_header)

# carousel:--------------------------------------------------------------------


class Carousel(BootstrapContainer):
    _default_class_name = "carousel slide"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None,
                 with_controls: bool = False,
                 with_indicators: bool = False,
                 fade_animation: bool = False) -> None:

        super().__init__(inner_html=inner_html, id=id, class_name=class_name, parent=parent)

        self.set_attribute("data-bs-ride", "carousel")

        if fade_animation:
            self.add_class("carousel-fade")

        self._controls = None
        self._control_prev = None
        self._control_next = None
        self._indicators = None
        self._carousel_inner = BootstrapContainer(
            class_name="carousel-inner", parent=self)

        self._slides = []

        if with_controls:
            self._controls = BootstrapContainer(
                class_name="carousel-controls", parent=self)
            self._control_prev = HTML.Button(
                class_name="carousel-control-prev", parent=self._controls)
            self._control_prev.set_attribute("data-bs-target", "#" + self.id)
            self._control_prev.set_attribute("data-bs-slide", "prev")
            self._control_prev.set_attribute("aria-label", "Previous")

            prev_icon = HTML.Span(
                class_name="carousel-control-prev-icon", parent=self._control_prev)
            prev_icon.set_attribute("aria-hidden", "true")

            HTML.Span(class_name="visually-hidden", parent=self._control_prev)

            self._control_next = HTML.Button(
                class_name="carousel-control-next", parent=self._controls)
            self._control_next.set_attribute("data-bs-target", "#" + self.id)
            self._control_next.set_attribute("data-bs-slide", "next")
            self._control_next.set_attribute("aria-label", "Next")

            next_icon = HTML.Span(
                class_name="carousel-control-next-icon", parent=self._control_next)
            next_icon.set_attribute("aria-hidden", "true")

            HTML.Span(class_name="visually-hidden", parent=self._control_next)

        if with_indicators:

            self._indicators = BootstrapContainer(
                class_name="carousel-indicators", parent=self)

    def add_slide(self, slide: BootstrapContainer, is_active: bool = False, interval: int = None) -> None:
        item = HTML.Div(parent=self._carousel_inner)
        item.add_class("carousel-item")
        if is_active:
            item.add_class("active")

        if interval is not None:
            item.set_attribute("data-bs-interval", str(interval))

        slide.display_property = DisplayProperty.BLOCK
        slide.w = 100

        item.append_child(slide)
        self._slides.append(item)

        if self._indicators is not None:
            indicator = HTML.Button(parent=self._indicators)
            indicator.set_attribute("data-bs-target", "#" + self.id)
            indicator.set_attribute(
                "data-bs-slide-to", str(len(self._slides) - 1))
            if is_active:
                indicator.add_class("active")
                indicator.set_attribute("aria-current", "true")

            self.set_attribute("data-bs-interval", "false")
            self.set_attribute("aria-label", "Slide " +
                               str(len(self._slides) - 1))
        return item


class CarouselDark(Carousel):
    _default_class_name = "carousel carousel-dark slide"


class DropdownButton(BootstrapContainer):

    _default_class_name: str = "dropdown"

    _default_dropdown_menu_class: str = "dropdown-menu"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 custom_title: str = None,
                 title_is_value: bool = True,
                 options: List[str] = None,
                 button_class=ButtonPrimary,
                 option_callback=None,
                 fire_callback_on_options_change: bool = True,
                 parent: HTML.Element = None,
                 inner_html: str = None,) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        self._dropdown_button = None
        self._dropdown_list = None
        self._options = None
        self._callback_function = option_callback
        self._title_is_value = title_is_value
        self._custom_title = custom_title
        self._fire_callback_on_options_change = fire_callback_on_options_change
        self._button_class = button_class

        self._current_value = None

        self._create_dropdown_button(custom_title, button_class)
        self._create_options(options)

    def _create_dropdown_button(self, title: str, button_class) -> None:
        self._dropdown_button = button_class(inner_html=title, parent=self)
        self._dropdown_button.add_class("dropdown-toggle")
        self._dropdown_button.set_attribute("data-bs-toggle", "dropdown")
        self._dropdown_button.set_attribute("aria-expanded", "false")

    def _create_options(self, options):
        self._dropdown_list = BootstrapContainer(
            class_name=self.__class__._default_dropdown_menu_class, parent=self)
        self._dropdown_list.set_attribute(
            "aria-labelledby", self._dropdown_button.id)
        self._options = []
        for option in options:
            option_button = self._button_class(
                inner_html=option, parent=self._dropdown_list)
            option_button.add_class("dropdown-item")
            self._options.append(option)
            option_button.onclick = lambda _, opt=option: self._on_option_click(
                opt)

        if self._fire_callback_on_options_change:
            self._on_option_click(options[0])

    def _on_option_click(self, option) -> None:
        if self._callback_function is not None:
            self._callback_function(option)
        if self._title_is_value and self._custom_title is None:
            self.title = option

        self._current_value = option

    @property
    def title(self) -> str:
        return self._dropdown_button.inner_html

    @title.setter
    def title(self, title: str) -> None:
        self._dropdown_button.inner_html = title

    @property
    def options(self) -> List[str]:
        return self._options

    @options.setter
    def options(self, options: List[str]) -> None:
        self._dropdown_list.destroy()
        self._create_options(options)

    @property
    def current_value(self) -> str:
        return self._current_value

    @current_value.setter
    def current_value(self, value: str) -> None:
        if value not in self._options:
            raise ValueError("Value not in options")
        self._on_option_click(value)


class DropdownButtonDark(DropdownButton):

    _default_dropdown_menu_class: str = "dropdown-menu dropdown-menu-dark"


# containers ------------------------------------------------------------------


class ContainerSmall(BootstrapContainer):
    _default_class_name = "container-sm"


class ContainerMedium(BootstrapContainer):
    _default_class_name = "container-md"


class ContainerLarge(BootstrapContainer):
    _default_class_name = "container-lg"


class ContainerXL(BootstrapContainer):
    _default_class_name = "container-xl"


class ContainerXXL(BootstrapContainer):
    _default_class_name = "container-xxl"


class ContainerFluid(BootstrapContainer):
    _default_class_name = "container-fluid"


class Row(BootstrapContainer):
    _default_class_name = "row"


class Col(BootstrapContainer):

    _default_class_name = "col"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 col: int = None,
                 col_sm: int = None,
                 col_md: int = None,
                 col_lg: int = None,
                 col_xl: int = None,
                 col_xxl: int = None) -> None:

        if col is not None:
            self.col = col

        super().__init__(inner_html, id, class_name, parent)

        if col_sm is not None:
            self.col_sm = col_sm

        if col_md is not None:
            self.col_md = col_md

        if col_lg is not None:
            self.col_lg = col_lg

        if col_xl is not None:
            self.col_xl = col_xl

        if col_xxl is not None:
            self.col_xxl = col_xxl

    @property
    def order(self) -> Union[str, int, None]:
        orders = list(self._search_class_list("order-{}"))
        if len(orders) == 0:
            return None
        order = orders[0]   # ignore other orders than the first one
        _, number = order.split("-")

        if number.isnumeric():
            return int(number)
        return number

    @order.setter
    def order(self, value: Union[str, int, None]) -> None:
        self._remove_classes_by_search_term("order-{}")
        if value is not None:
            self.add_class(f"order-{str(value)}")


class ListGroup(HTML.Ul, BootstrapContainer):
    _default_class_name = "list-group"

    def __init__(self, id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None,
                 items: List[Union[str, HTML.Element]] = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        if items is not None:
            for item in items:
                self.add_item(item)

    def add_item(self, item: Union[str, HTML.Element], active: bool = False, disabled: bool = False, item_class=HTML.Li) -> None:
        li = item_class(class_name="list-group-item", parent=self)
        if active:
            li.add_class("active")
        if disabled:
            li.add_class("disabled")
        if isinstance(item, str):
            li.inner_html = item
        else:
            li.append(item)

        return li


class ListGroupSelectable(ListGroup):

    def __init__(self, id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None,
                 options: List[Union[HTML.Element, str]] = None,
                 button_class=ButtonPrimary) -> None:

        self._button_class = button_class
        self._items = []
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent,
                         items=options)

    def add_item(self, item: Union[str, HTML.Element],
                 active: bool = False,
                 disabled: bool = False) -> None:
        item = super().add_item(item,
                                active,
                                disabled,
                                item_class=self._button_class)

        item.add_class("list-group-item-action")
        self._items.append(item)

        item.onclick = lambda _, item=item: item.set_class(
            "active", not item.has_class("active"))
        return item

    @property
    def selected_options(self) -> List[str]:

        selected = []
        for item in self._items:
            if item.has_class("active"):
                selected.append(item.inner_html)
                # TODO: will not work for html items
        return selected

# modal: ----------------------------------------------------------------------


class ModalTitle(HTML.H5, BootstrapContainer):
    _default_class_name: str = "modal-title"

    def __init__(self, title: str,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        self.inner_html = title


class ModalHeader(BootstrapContainer):

    _default_class_name: str = "modal-header"

    def __init__(self,
                 title: Union[str, HTML.Element],
                 has_close_button: bool = True,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        self._title = None
        self._close_button = None

        if title is not None:
            if isinstance(title, str):
                self._title = ModalTitle(title, parent=self)
            else:
                self._title = title
                self.append(title)

        if has_close_button:
            self._button = Button(class_name="btn-close", parent=self)
            self._button.set_attribute("data-bs-dismiss", "modal")
            self._button.set_attribute("aria-label", "Close")


class ModalBody(BootstrapContainer):

    _default_class_name: str = "modal-body"


class ModalFooter(BootstrapContainer):

    _default_class_name: str = "modal-footer"


class ModalContent(BootstrapContainer):

    _default_class_name: str = "modal-content"


class ModalDialog(BootstrapContainer):

    _default_class_name: str = "modal-dialog"


class Modal(BootstrapContainer):

    _default_class_name: str = "modal"

    def __init__(self,
                 title: Union[str, HTML.Element],
                 has_close_button: bool = True,
                 fade: bool = True,
                 static_backdrop: bool = False,
                 modal_scrollable: bool = False,
                 vertically_centered: bool = False,
                 body: Union[str, HTML.Element] = None,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        self.set_attribute("tabindex", -1)
        if fade:
            self.add_class("fade")

        if static_backdrop:
            self.set_attribute("data-bs-backdrop", "static")

        self._modal_dialog = ModalDialog(parent=self)

        if modal_scrollable:
            self._modal_dialog.add_class("modal-dialog-scrollable")

        if vertically_centered:
            self._modal_dialog.add_class("modal-dialog-centered")

        self._modal_content = ModalContent(parent=self._modal_dialog)

        self._header = ModalHeader(
            parent=self._modal_content, title=title, has_close_button=has_close_button)
        self._body = ModalBody(parent=self._modal_content)
        self._body.append_child(body)
        self._footer = ModalFooter(parent=self._modal_content)

        self._js_modal = bootstrap.Modal.new(self.element)

    @property
    def header(self) -> ModalHeader:
        return self._header

    @property
    def body(self) -> ModalBody:
        return self._body

    @property
    def footer(self) -> ModalFooter:
        return self._footer

    def show(self) -> None:
        # TODO: maybe modify elements directly?
        self._js_modal.show()

    def hide(self) -> None:
        self._js_modal.hide()

    def toggle(self) -> None:
        self._js_modal.toggle()


# navbar: ---------------------------------------------------------------------

class NavItem(HTML.Li, BootstrapContainer):
    _default_class_name: str = "nav-item"


class NavList(HTML.Ul, BootstrapContainer):

    _default_class_name: str = "nav"

    def add_item(self, item: HTML.Element):
        li_item = NavItem(parent=self)
        li_item.append_child(item)

    @property
    def nav_fill(self) -> None:
        self.has_class("nav-fill")

    @nav_fill.setter
    def nav_fill(self, value: bool) -> None:
        if value:
            self.add_class("nav-fill")
        else:
            self.remove_class("nav-fill")


class NavListVertical(NavList):

    _default_class_name: str = "nav flex-column"


class NavListTabs(NavList):

    _default_class_name: str = "nav nav-tabs"


class NavListPills(NavList):

    _default_class_name: str = "nav nav-pills"


class NavbarBrand(HTML.A, BootstrapContainer):
    _default_class_name: str = "navbar-brand"

    def __init__(self,
                 text: str,
                 href: str = "#",
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None) -> None:
        super().__init__(inner_html=text,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        self.set_attribute("href", href)


class Navbar(BootstrapContainer):

    _default_class_name: str = "navbar"
    _default_nav_list_class = NavList

    def __init__(self,
                 options: List[str] = None,
                 brand: Union[str, NavbarBrand] = None,
                 option_callback: Callable = None,
                 fire_callback_on_option_init: bool = True,
                 nav_fill: bool = False,
                 justification: JustifyContent = JustifyContent.START,
                 toggle_button_for_target: HTML.Element = None,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        if toggle_button_for_target is not None:
            nav_item = NavItem(parent=self)
            hamburger = ButtonHamburger(parent=nav_item)
            hamburger.make_collapse_toggle(toggle_button_for_target)

        if brand is not None:
            self._brand = brand if isinstance(
                brand, NavbarBrand) else NavbarBrand(brand)
            self.append_child(self._brand)

        self._nav_list = self.__class__._default_nav_list_class(parent=self)
        self._nav_list.justify_content = justification
        self._nav_list.nav_fill = nav_fill
        if nav_fill:
            self.add_class("navbar-expand-lg")

        self._options = {}
        self._current_nav_link = None
        self._current_nav_name = None
        self._fire_callback_on_option_init = fire_callback_on_option_init

        self._option_callback = option_callback

        if isinstance(brand, str):
            self._brand = HTML.A(brand, parent=self)
        else:
            self._brand = brand
            self.append_child(brand)

        self._nav_list.add_item(self._brand)

        if options is not None:
            for option in options:
                self.add_nav_option(option)

        if options is not None:
            self._on_click(options[0])

    def add_item(self, item: HTML.Element):
        self._nav_list.add_item(item)

    def _activate_nav_link(self, nav_link, nav_name):
        if self._current_nav_link is not None:
            self._current_nav_link.remove_class("active")
            self._current_nav_link.remove_attribute("aria-current")
        self._current_nav_link = nav_link
        self._current_nav_link.add_class("active")
        self._current_nav_link.set_attribute("aria-current", "page")

        self._current_nav_name = nav_name

    def _deactivate_nav_link(self):
        if self._current_nav_link is not None:
            self._current_nav_link.remove_class("active")
            self._current_nav_link.remove_attribute("aria-current")
        self._current_nav_link = None
        self._current_nav_name = None

    def _on_click(self, option: str, fire_callback: bool = True):
        self._activate_nav_link(self._options[option], option)
        if fire_callback and self._option_callback is not None:
            self._option_callback(option)

    def add_nav_option(self, option: str, is_active: bool = False):
        link = Button(option, class_name="nav-link", parent=self._nav_list)
        self._nav_list.add_item(link)
        self._options[option] = link

        if is_active:
            self._on_click(
                option, fire_callback=self._fire_callback_on_option_init)

        link.onclick = lambda _, option=option: self._on_click(option)

    @property
    def current_nav_option(self) -> Union[str, None]:
        return self._current_nav_name

    @property
    def option_callback(self) -> Callable:
        return self._option_callback

    @option_callback.setter
    def option_callback(self, value: Callable) -> None:
        self._option_callback = value


class NavbarVertical(Navbar):

    _default_nav_list_class = NavListVertical


class NavbarTabs(Navbar):

    _default_nav_list_class = NavListTabs


class NavbarPills(Navbar):

    _default_nav_list_class = NavListPills


class NavbarDark(Navbar):

    _default_class_name: str = "navbar navbar-dark bg-dark"


class NavbarVerticalDark(NavbarVertical):

    _default_class_name: str = "navbar navbar-dark bg-dark"


class NavbarTabsDark(NavbarTabs):

    _default_class_name: str = "navbar navbar-dark bg-dark"


class NavbarPillsDark(NavbarPills):

    _default_class_name: str = "navbar navbar-dark bg-dark"


class Tabs(BootstrapContainer):

    _default_navbar_tabs_class = NavbarTabs

    def __init__(self,
                 contents: Dict[str, BootstrapContainer],
                 navbar: Navbar = None,
                 id: str = None,
                 class_name: str = None,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         id=id,
                         class_name=class_name,
                         parent=parent)

        if navbar is None:
            navbar = self.__class__._default_navbar_tabs_class(
                options=list(contents.keys()))

        self._navbar = navbar
        self.append_child(self._navbar)

        self._content_container = BootstrapContainer(parent=self)
        self._content_container.w = 100
        self._content_container.h = 100

        self._active_tab: str = None
        self._contents = contents

        for content in contents.values():
            self._content_container.append_child(content)
            content.add_class("d-none")

        self._old_navbar_callback = self._navbar.option_callback
        self._navbar._option_callback = self._tab_click_callback

        self.active_tab = list(contents.keys())[0]

    def _tab_click_callback(self, tab_name: str):
        self._activate_tab(tab_name)
        if self._old_navbar_callback is not None:
            self._old_navbar_callback(tab_name)

    def _activate_tab(self, tab: str):
        if self._active_tab is not None:
            self._contents[self._active_tab].add_class("d-none")
        self._active_tab = tab
        self._contents[self._active_tab].remove_class("d-none")

    @property
    def active_tab(self) -> Union[str, None]:
        return self._active_tab

    @active_tab.setter
    def active_tab(self, value: str) -> None:
        self._activate_tab(value)


class TabsDark(Tabs):

    _default_navbar_tabs_class = NavbarTabsDark

class ToastHeader(BootstrapContainer):

    _default_class_name = "toast-header"

    def __init__(self, title:str,
                       inner_html: str = None,
                       id: str = None,
                       class_name: str = None,
                       parent: "Element" = None) -> None:
        super().__init__(inner_html=inner_html, id=id, class_name=class_name, parent=parent)

        HTML.Strong(title, class_name="me-auto", parent=self)
        close_button = HTML.Button(class_name="btn-close", parent=self)
        close_button.set_attribute("data-bs-dismiss", "toast")
        close_button.set_attribute("aria-label", "Close")

class ToastBody(BootstrapContainer):
    _default_class_name: str = "toast-body"

class Toast(BootstrapContainer):

    _default_class_name: str = "toast"

    def __init__(self, inner_html: str = None,
                       title: str = "Toast",
                       id: str = None,
                       class_name: str = None,
                       parent: "Element" = None) -> None:

        super().__init__(id=id, class_name=class_name, parent=parent)

        self.set_attribute("role", "alert")
        self.set_attribute("aria-live", "assertlive")
        self.set_attribute("aria-atomic", True)
        self.p = 2

        ToastHeader(title, parent=self)
        ToastBody(inner_html, parent=self)

        self._js_toast = bootstrap.Toast.new(self.element)
    
    def show(self):
        self._js_toast.show()
    
    def hide(self):
        self._js_toast.hide()
    
    def dispose(self):
        self._js_toast.dispose()
    
    @property
    def animation(self) -> bool:
        return self.get_attribute("data-bs-animation", is_boolean_attribute=True)
    
    @animation.setter
    def animation(self, value:bool):
        self.set_attribute("data-bs-animation", attribute_value=value ,is_boolean_attribute=True)
    
    @property
    def autohide(self) -> bool:
        return self.get_attribute("data-bs-autohide", is_boolean_attribute=True)
    
    @autohide.setter
    def autohide(self, value:bool):
        self.set_attribute("data-bs-autohide", attribute_value=value ,is_boolean_attribute=True)
    
    @property
    def delay(self) -> bool:
        return self.get_attribute("data-bs-delay", is_boolean_attribute=True)
    
    @delay.setter
    def delay(self, value:bool):
        self.set_attribute("data-bs-delay", attribute_value=value ,is_boolean_attribute=True)

class ToastContainer(BootstrapContainer):
    _default_class_name: str = "toast-container"

    def __init__(self, inner_html: str = None,
                       id: str = None,
                       class_name: str = None,
                       parent: "Element" = None) -> None:

        super().__init__(inner_html=inner_html, id=id, class_name=class_name, parent=parent)

        self.position = Position.ABSOLUTE
        self.p = 3
    
    def show_toast(self, toast: Toast):
        self.append_child(toast)
        toast.show()

class OffcanvasTitle(HTML.H5, BootstrapContainer):

    _default_class_name: str = "offcanvas-title"


class OffcanvasHeader(BootstrapContainer):

    _default_class_name: str = "offcanvas-header"

    def __init__(self,
                 title: Union[str, OffcanvasTitle],
                 close_button:bool = True,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         parent=parent)

        if isinstance(title, str):
            title = OffcanvasTitle(title)
        self.append_child(title)

        if close_button:
            btn = Button(class_name="btn-close text-reset")
            btn.set_attribute("aria-label", "Close")
            btn.set_attribute("data-bs-dismiss", "offcanvas")
            self.append_child(btn)


class OffcanvasBody(BootstrapContainer):

    _default_class_name: str = "offcanvas-body"

class Offcanvas(BootstrapContainer):

    _default_class_name: str = "offcanvas offcanvas-start"

    def __init__(self,
                 header: Union[str, OffcanvasHeader],
                 content = HTML.Element,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         parent=parent)


        self.set_attribute("tabindex", "-1")

        self._js_offcanvas = bootstrap.Offcanvas.new(self.element)

        if isinstance(header, str):
            header = OffcanvasHeader(header)

        self._header = header
        self.append_child(header)

        self._body = OffcanvasBody(parent=self)
        self._body.append_child(content)
    
    def show(self):
        self._js_offcanvas.show()
    
    def hide(self) -> None:
        self._js_offcanvas.hide()
    
    def toggle(self) -> None:
        self._js_offcanvas.toggle()
    
class OffcanvasStart(Offcanvas):

    pass

class OffcanvasTop(Offcanvas):

    _default_class_name: str = "offcanvas offcanvas-top"

class OffcanvasEnd(Offcanvas):

    _default_class_name: str = "offcanvas offcanvas-end"

class OffcanvasBottom(Offcanvas):

    _default_class_name: str = "offcanvas offcanvas-bottom"


class Progress(BootstrapContainer):

    _default_class_name: str = "progress"

    def __init__(self,
                 value: int = 0,
                 max: int = 100,
                 striped: bool = True,
                 animated: bool = True,
                 parent: HTML.Element = None,
                 inner_html: str = None) -> None:
        super().__init__(inner_html=inner_html,
                         parent=parent)

        self._value = value
        self._max = max

        self._progress_bar = BootstrapContainer(parent=self, class_name="progress-bar")
        
        self.is_striped = striped
        self.is_animated = animated

        self._update_progress_bar()



    def _update_progress_bar(self):
        self._progress_bar.set_attribute("role", "progressbar")
        self._progress_bar.set_attribute("aria-valuenow", str(self._value))
        self._progress_bar.set_attribute("aria-valuemin", "0")
        self._progress_bar.set_attribute("aria-valuemax", str(self._max))
        self._progress_bar.set_attribute("style", "width: " + str(int(100 * self._value / self._max)) + "%")

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value
        self._update_progress_bar()

    @property
    def max(self) -> int:
        return self._max

    @max.setter
    def max(self, value: int) -> None:
        self._max = value
        self._update_progress_bar()
    
    @property
    def is_striped(self) -> bool:
        return self._progress_bar.has_class("progress-bar-striped")
    
    @is_striped.setter
    def is_striped(self, value: bool) -> None:
        self._progress_bar.set_class("progress-bar-striped", value)
    
    @property
    def is_animated(self) -> bool:
        return self._progress_bar.has_class("progress-bar-animated")
    
    @is_animated.setter
    def is_animated(self, value: bool) -> None:
        self._progress_bar.set_class("progress-bar-animated", value)

