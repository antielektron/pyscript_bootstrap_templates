
from typing import Callable, Iterable, Union
import uuid
from js import document, CanvasRenderingContext2D  # type: ignore
from pyodide import create_proxy  # type: ignore
from parse import *
import numpy as np
import base64
from PIL import Image as PILImage
from io import BytesIO, StringIO


class Element(object):

    _tag_type: str = None
    _default_class_name: str = None

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: "Element" = None) -> None:
        self._parent = None
        self._class_name = class_name if class_name is not None else self._default_class_name
        self._children = []

        if id is None:
            self._id = "id-" + str(uuid.uuid4())
            # TODO: use a better id generator
        else:
            self._id = id

        self._element = None

        self._display = None

        self._init_element()

        if parent is not None:
            parent.append_child(self)

        if inner_html is not None:
            self.inner_html = inner_html

    def _init_element(self):
        if self.tag_type is None:
            raise NotImplementedError("tag_type is not implemented")

        if self._element is None:
            self._element = document.createElement(self.tag_type)
            self._element.id = self._id
            if self._class_name is not None:
                self._element.className = self._class_name
        return self._element

    def append_child(self, child: "Element") -> None:
        if child is None:
            return
        self._children.append(child)
        child._parent = self
        self._element.appendChild(child._element)

    def remove_child(self, child: "Element") -> None:
        self._children.remove(child)
        self._element.removeChild(child._element)
        child._parent = None

    def hide(self) -> None:
        self._display = self.element.style.display
        self.element.style.display = "none"

    def show(self) -> None:
        if self._display is None:
            return
        self.element.style.display = self._display
        self._display = None

    def destroy(self) -> None:
        if self._parent is not None:
            self._parent.remove_child(self)
        for c in self.children:
            c.destroy()
        self._children = []
        self._element.remove()
        self._element = None
        self._parent = None
        

    def add_event_listener(self, event_name: str, callback: callable) -> None:
        self._element.addEventListener(event_name,
                                       create_proxy(callback))

    def set_class(self, class_name: str, active: bool) -> None:
        if active:
            self.add_class(class_name=class_name)
        else:
            self.remove_class(class_name=class_name)

    def add_class(self, class_name: Union[str, None]) -> None:
        if class_name is None:
            return
        self._element.classList.add(class_name)

    def add_classes(self, *class_names: str) -> None:
        for class_name in class_names:
            self.add_class(class_name)

    def has_class(self, class_name: str) -> bool:
        return self._element.classList.contains(class_name)

    def remove_class(self, class_name: str) -> None:
        self._element.classList.remove(class_name)

    def remove_classes(self, *class_names: str) -> None:
        for class_name in class_names:
            self.remove_class(class_name)

    def has_attribute(self, attribute_name: str) -> bool:
        return self._element.hasAttribute(attribute_name)

    def set_attribute(self, attribute_name: str, attribute_value: Union[object, None], is_boolean_attribute: bool = False) -> None:

        if attribute_value is None:
            self.remove_attribute(attribute_name)
            return

        if is_boolean_attribute:
            if attribute_value:
                self._element.setAttribute(attribute_name, "")
            else:
                self._element.removeAttribute(attribute_name)
        else:
            self._element.setAttribute(attribute_name, attribute_value)

    def remove_attribute(self, attribute_name: str) -> None:
        self._element.removeAttribute(attribute_name)

    def get_attribute(self, attribute_name: str, is_boolean_attribute: bool = False) -> Union[str, None]:
        if is_boolean_attribute:
            return self._element.hasAttribute(attribute_name)
        elif self._element.hasAttribute(attribute_name):
            return self._element.getAttribute(attribute_name)
        return None

    @property
    def parent(self) -> "Element":
        return self._parent

    @property
    def children(self) -> list:
        return self._children

    @property
    def tag_type(self) -> str:
        return self._tag_type

    @property
    def element(self):
        return self._element

    @property
    def inner_html(self):
        return self._element.innerHTML

    @inner_html.setter
    def inner_html(self, value: str):
        self._element.innerHTML = value

    @property
    def class_name(self):
        return self._class_name

    @class_name.setter
    def class_name(self, value: str):
        self._class_name = value
        self._element.className = value

    @property
    def class_list(self):
        return self._element.classList

    @property
    def width(self):
        return self._element.style.width

    @width.setter
    def width(self, value: str):
        self._element.style.width = value

    @property
    def height(self):
        return self._element.style.height

    @height.setter
    def height(self, value: str):
        self._element.style.height = value

    def _search_class_list(self, search_term: str) -> Iterable:
        classes = self.class_list
        # TODO: use compiled parse objects to make it faster?
        return filter(lambda x: parse(search_term, x) is not None, classes)

    def _remove_classes_by_search_term(self, search_term) -> None:
        for css_class in self._search_class_list(search_term=search_term):
            self.remove_class(css_class)

    @property
    def id(self):
        return self._id
    
    def write(self, object):
        self.element.write(self.id, object) # type: ignore


class A(Element):

    _tag_type: str = "a"

    def __init__(self, inner_html: str = None, id: str = None, class_name: str = None, parent: Element = None, href: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if href is not None:
            self.href = href

    @property
    def href(self) -> str:
        return self.get_attribute("href")

    @href.setter
    def href(self, value: str) -> None:
        self.set_attribute("href", value)


class Abbr(Element):

    _tag_type: str = "abbr"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 title: str = None,
                 class_name: str = None,
                 parent: Element = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if title is not None:
            self.title = title

    @property
    def title(self) -> str:
        return self.get_attribute("title")

    @title.setter
    def title(self, value: str) -> None:
        self.set_attribute("title", value)


class Address(Element):

    _tag_type: str = "address"


class Area(Element):

    _tag_type: str = "area"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 alt: str = None,
                 coords: str = None,
                 href: str = None,
                 shape: str = None,
                 target: str = None,
                 type: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if alt is not None:
            self.alt = alt
        if coords is not None:
            self.coords = coords
        if href is not None:
            self.href = href
        if shape is not None:
            self.shape = shape
        if target is not None:
            self.target = target
        if type is not None:
            self.type = type

    @property
    def alt(self) -> str:
        return self.get_attribute("alt")

    @alt.setter
    def alt(self, value: str) -> None:
        self.set_attribute("alt", value)

    @property
    def coords(self) -> str:
        return self.get_attribute("coords")

    @coords.setter
    def coords(self, value: str) -> None:
        self.set_attribute("coords", value)

    @property
    def href(self) -> str:
        return self.get_attribute("href")

    @href.setter
    def href(self, value: str) -> None:
        self.set_attribute("href", value)

    @property
    def shape(self) -> str:
        return self.get_attribute("shape")

    @shape.setter
    def shape(self, value: str) -> None:
        self.set_attribute("shape", value)

    @property
    def target(self) -> str:
        return self.get_attribute("target")

    @target.setter
    def target(self, value: str) -> None:
        self.set_attribute("target", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)


class Article(Element):

    _tag_type: str = "article"


class Aside(Element):

    _tag_type: str = "aside"


class Audio(Element):

    @classmethod
    def from_file(cls, file_path: str, format: str) -> "Audio":
        bytes = open(file_path, "rb").read()

        src = "data:audio/{};base64,{}".format(format, base64.b64encode(bytes).decode("utf-8"))

        return cls(src=src)

    _tag_type: str = "audio"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: "Element" = None,
                 autoplay: bool = False,
                 controls: bool = False,
                 loop: bool = False,
                 muted: bool = False,
                 preload: str = None,
                 src: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        self.autoplay = autoplay
        self.controls = controls
        self.loop = loop
        self.muted = muted

        if preload is not None:
            self.preload = preload

        if src is not None:
            self.src = src

    @property
    def autoplay(self) -> bool:
        return self.get_attribute("autoplay", is_boolean_attribute=True)

    @autoplay.setter
    def autoplay(self, value: bool) -> None:
        self.set_attribute("autoplay", value, is_boolean_attribute=True)

    @property
    def controls(self) -> bool:
        return self.get_attribute("controls", is_boolean_attribute=True)

    @controls.setter
    def controls(self, value: bool) -> None:
        self.set_attribute("controls", value, is_boolean_attribute=True)

    @property
    def loop(self) -> bool:
        return self.get_attribute("loop", is_boolean_attribute=True)

    @loop.setter
    def loop(self, value: bool) -> None:
        self.set_attribute("loop", value, is_boolean_attribute=True)

    @property
    def muted(self) -> bool:
        return self.get_attribute("muted", is_boolean_attribute=True)

    @muted.setter
    def muted(self, value: bool) -> None:
        self.set_attribute("muted", value, is_boolean_attribute=True)

    @property
    def preload(self) -> str:
        return self.get_attribute("preload")

    @preload.setter
    def preload(self, value: str) -> None:
        self.set_attribute("preload", value)

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)


class B(Element):

    _tag_type: str = "b"


class Base(Element):

    _tag_type: str = "base"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 href: str = None,
                 target: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        if href is not None:
            self.href = href
        if target is not None:
            self.target = target

    @property
    def href(self) -> str:
        return self.get_attribute("href")

    @href.setter
    def href(self, value: str) -> None:
        self.set_attribute("href", value)

    @property
    def target(self) -> str:
        return self.get_attribute("target")

    @target.setter
    def target(self, value: str) -> None:
        self.set_attribute("target", value)


class Bdi(Element):

    _tag_type: str = "bdi"


class Blockquote(Element):

    _tag_type: str = "blockquote"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 cite: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if cite is not None:
            self.cite = cite

    @property
    def cite(self) -> str:
        return self.get_attribute("cite")

    @cite.setter
    def cite(self, value: str) -> None:
        self.set_attribute("cite", value)


class Body(Element):

    _tag_type: str = "body"


class Br(Element):

    _tag_type: str = "br"


class Button(Element):

    _tag_type: str = "button"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: "Element" = None,
                 type: str = "button",
                 name: str = None,
                 value: str = None,
                 onclick=None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        self._onclick = None

        self.type = type

        if name is not None:
            self.name = name

        if value is not None:
            self.value = value

        if onclick is not None:
            self.onclick = onclick

    def disable(self) -> None:
        self._element.disabled = True

    def enable(self) -> None:
        self._element.disabled = False

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def value(self) -> str:
        return self.get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        self.set_attribute("value", value)

    @property
    def disabled(self) -> bool:
        self.get_attribute("disabled", is_boolean_attribute=True)

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.set_attribute("disabled", value, is_boolean_attribute=True)

    @property
    def onclick(self) -> str:
        return self._onclick

    @onclick.setter
    def onclick(self, value) -> None:
        self._onclick = value
        self.add_event_listener("click", value)


class Canvas(Element):

    _tag_type: str = "canvas"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 width: int = None,
                 height: int = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    @property
    def width(self) -> int:
        return self.get_attribute("width")

    @width.setter
    def width(self, value: int) -> None:
        self.set_attribute("width", value)

    @property
    def height(self) -> int:
        return self.get_attribute("height")

    @height.setter
    def height(self, value: int) -> None:
        self.set_attribute("height", value)

    @property
    def get_context(self) -> CanvasRenderingContext2D:
        return self._element.getContext("2d")


class Caption(Element):

    _tag_type: str = "caption"


class Citation(Element):

    _tag_type: str = "cite"


class Code(Element):

    _tag_type: str = "code"


class Col(Element):

    _tag_type: str = "col"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 span: int = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        if span is not None:
            self.span = span

    @property
    def span(self) -> int:
        return self.get_attribute("span")

    @span.setter
    def span(self, value: int) -> None:
        self.set_attribute("span", value)


class Colgroup(Element):

    _tag_type: str = "colgroup"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 span: int = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        if span is not None:
            self.span = span

    @property
    def span(self) -> int:
        return self.get_attribute("span")

    @span.setter
    def span(self, value: int) -> None:
        self.set_attribute("span", value)


class Data(Element):

    _tag_type: str = "data"


class DataList(Element):

    _tag_type: str = "datalist"


class Dd(Element):

    _tag_type: str = "dd"


class Del(Element):

    _tag_type: str = "del"


class Details(Element):

    _tag_type: str = "details"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 open: bool = False) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        self.open = open

    @property
    def open(self) -> bool:
        return self.get_attribute("open", is_boolean_attribute=True)

    @open.setter
    def open(self, value: bool) -> None:
        self.set_attribute("open", value, is_boolean_attribute=True)


class Dfn(Element):

    _tag_type: str = "dfn"


class Dialog(Element):

    _tag_type: str = "dialog"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 open: bool = False) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent)

        self.open = open

    @property
    def open(self) -> bool:
        return self.get_attribute("open", is_boolean_attribute=True)

    @open.setter
    def open(self, value: bool) -> None:
        self.set_attribute("open", value, is_boolean_attribute=True)


class Div(Element):

    _tag_type: str = "div"


class Dt(Element):

    _tag_type: str = "dt"


class Dl(Element):

    _tag_type: str = "dl"


class Em(Element):

    _tag_type: str = "em"


class Embed(Element):

    _tag_type: str = "embed"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 src: str = None,
                 type: str = None,
                 width: int = None,
                 height: int = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if src is not None:
            self.src = src
        if type is not None:
            self.type = type
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

    @property
    def width(self) -> int:
        return self.get_attribute("width")

    @width.setter
    def width(self, value: int) -> None:
        self.set_attribute("width", value)

    @property
    def height(self) -> int:
        return self.get_attribute("height")

    @height.setter
    def height(self, value: int) -> None:
        self.set_attribute("height", value)


class Fieldset(Element):

    _tag_type: str = "fieldset"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 disabled: bool = False,
                 form_id: str = None,
                 name: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        self.disabled = disabled
        self.form_id = form_id
        self.name = name

    @property
    def disabled(self) -> bool:
        return self.get_attribute("disabled", is_boolean_attribute=True)

    @disabled.setter
    def disabled(self, value: bool) -> None:
        self.set_attribute("disabled", value, is_boolean_attribute=True)

    # TODO: add form as html object

    @property
    def form_id(self) -> str:
        return self.get_attribute("form")

    @form_id.setter
    def form_id(self, value: str) -> None:
        self.set_attribute("form", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)


class Figcaption(Element):

    _tag_type: str = "figcaption"


class Figure(Element):

    _tag_type: str = "figure"


class Footer(Element):

    _tag_type: str = "footer"


class Form(Element):

    _tag_type: str = "form"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 action: str = None,
                 method: str = None,
                 name: str = None,
                 target: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if action is not None:
            self.action = action
        if method is not None:
            self.method = method
        if name is not None:
            self.name = name
        if target is not None:
            self.target = target

    @property
    def action(self) -> str:
        return self.get_attribute("action")

    @action.setter
    def action(self, value: str) -> None:
        self.set_attribute("action", value)

    @property
    def method(self) -> str:
        return self.get_attribute("method")

    @method.setter
    def method(self, value: str) -> None:
        self.set_attribute("method", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def target(self) -> str:
        return self.get_attribute("target")

    @target.setter
    def target(self, value: str) -> None:
        self.set_attribute("target", value)


class H1(Element):

    _tag_type: str = "h1"


class H2(Element):

    _tag_type: str = "h2"


class H3(Element):

    _tag_type: str = "h3"


class H4(Element):

    _tag_type: str = "h4"


class H5(Element):

    _tag_type: str = "h5"


class H6(Element):

    _tag_type: str = "h6"


class Head(Element):

    _tag_type: str = "head"


class Header(Element):

    _tag_type: str = "header"


class Hr(Element):

    _tag_type: str = "hr"


class Html(Element):

    _tag_type: str = "html"


class I(Element):

    _tag_type: str = "i"


class IFrame(Element):

    _tag_type: str = "iframe"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 src: str = None,
                 srcdoc: str = None,
                 name: str = None,
                 sandbox: str = None,
                 allow_fullscreen: bool = False,
                 inner_html: str = None) -> None:
        super().__init__(id=id,
                         class_name=class_name,
                         parent=parent,
                         inner_html=inner_html)

        if src is not None:
            self.src = src
        if srcdoc is not None:
            self.srcdoc = srcdoc
        if name is not None:
            self.name = name
        if sandbox is not None:
            self.sandbox = sandbox
        if allow_fullscreen is not None:
            self.allow_fullscreen = allow_fullscreen

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def srcdoc(self) -> str:
        return self.get_attribute("srcdoc")

    @srcdoc.setter
    def srcdoc(self, value: str) -> None:
        self.set_attribute("srcdoc", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def sandbox(self) -> str:
        return self.get_attribute("sandbox")

    @sandbox.setter
    def sandbox(self, value: str) -> None:
        self.set_attribute("sandbox", value)

    @property
    def allow_fullscreen(self) -> bool:
        return self.get_attribute("allow_fullscreen", is_boolean_attribute=True)

    @allow_fullscreen.setter
    def allow_fullscreen(self, value: bool) -> None:
        self.set_attribute("allow_fullscreen", value,
                           is_boolean_attribute=True)


class Image(Element):

    @classmethod
    def from_numpy_array(cls, m:np.ndarray, format="PNG", **kwargs):
        if format.upper() == "JPG":
            format = "JPEG"

        img = PILImage.fromarray(m)
        buf = BytesIO()

        img.save(buf, format=format.upper())

        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(buf.getvalue()).decode('ascii')}"

        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_pil_image(cls, img:PILImage, format="PNG", **kwargs):

        buf = BytesIO()

        img.save(buf, format=format.upper())

        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(buf.getvalue()).decode('ascii')}"

        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_bytes(cls, img:bytes, format="PNG", **kwargs):

        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(img).decode('ascii')}"

        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_base64(cls, img:str, format="PNG", **kwargs):

        img_base64 = f"data:image/{format.lower()};base64, {img}"

        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_file(cls, file_path:str, format="PNG", **kwargs):
        img = PILImage.open(file_path)
        buf = BytesIO()

        img.save(buf, format=format.upper())

        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(buf.getvalue()).decode('utf-8')}"

        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_bytesio(cls, buf:BytesIO, format="PNG", **kwargs):
            
        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(buf.getvalue()).decode('utf-8')}"
    
        return cls(src=img_base64, **kwargs)
    
    @classmethod
    def from_matplotlib_figure(cls, fig:"matplotlib.pyplot.Figure", format="PNG", **kwargs):
        buf = BytesIO()
        fig.savefig(buf, format=format.upper())

        img_base64 = f"data:image/{format.lower()};base64, {base64.b64encode(buf.getvalue()).decode('utf-8')}"

        return cls(src=img_base64, **kwargs)


    _tag_type: str = "img"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 src: str = None,
                 alt: str = None,
                 width: str = None,
                 height: str = None,
                 usemap: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if src is not None:
            self.src = src

        if alt is not None:
            self.alt = alt

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def alt(self) -> str:
        return self.get_attribute("alt")

    @alt.setter
    def alt(self, value: str) -> None:
        self.set_attribute("alt", value)

    @property
    def usemap(self) -> str:
        # TODO: use python html wrapper here
        return self.get_attribute("usemap")

    @usemap.setter
    def usemap(self, value: str) -> None:
        self.set_attribute("usemap", value)


class Input(Element):

    _tag_type: str = "input"

    def __init__(self,
                 inner_html: str = None,
                 id: str = None,
                 class_name: str = None,
                 parent: "Element" = None,
                 type: str = "text",
                 name: str = None,
                 value: str = None,
                 placeholder: str = None,
                 onchange: Callable = None,
                 required: bool = False) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        self.type = type

        if name is not None:
            self.name = name

        if value is not None:
            self.value = value

        if placeholder is not None:
            self.placeholder = placeholder
        
        self._onchange = None
        if onchange is not None:
            self.onchange = onchange

        self.required = required

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def value(self) -> str:
        return self.get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        self.set_attribute("value", value)

    @property
    def placeholder(self) -> str:
        return self.get_attribute("placeholder")

    @placeholder.setter
    def placeholder(self, value: str) -> None:
        self.set_attribute("placeholder", value)

    @property
    def required(self) -> bool:
        return self.get_attribute("required")

    @required.setter
    def required(self, value: bool) -> None:
        self.set_attribute("required", value)
    
    @property
    def onchange(self) -> str:
        return self._onchange

    @onchange.setter
    def onchange(self, value) -> None:
        self._onchange = value
        self.add_event_listener("change", value)


class Ins(Element):

    _tag_type: str = "ins"


class Kbd(Element):

    _tag_type: str = "kbd"


class Label(Element):

    _tag_type: str = "label"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 for_id: str = None,
                 form_id: str = None,
                 name: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if for_id is not None:
            self.for_id = for_id

        if form_id is not None:
            self.form_id = form_id

        if name is not None:
            self.name = name

    @property
    def for_id(self) -> str:
        return self.get_attribute("for")

    @for_id.setter
    def for_id(self, value: str) -> None:
        self.set_attribute("for", value)

    @property
    def form_id(self) -> str:
        return self.get_attribute("form")

    @form_id.setter
    def form_id(self, value: str) -> None:
        self.set_attribute("form", value)

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)


class Legend(Element):

    _tag_type: str = "legend"


class Li(Element):

    _tag_type: str = "li"


class Link(Element):

    _tag_type: str = "link"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 rel: str = None,
                 href: str = None,
                 type: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if rel is not None:
            self.rel = rel

        if href is not None:
            self.href = href

        if type is not None:
            self.type = type

    @property
    def rel(self) -> str:
        return self.get_attribute("rel")

    @rel.setter
    def rel(self, value: str) -> None:
        self.set_attribute("rel", value)

    @property
    def href(self) -> str:
        return self.get_attribute("href")

    @href.setter
    def href(self, value: str) -> None:
        self.set_attribute("href", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)


class Main(Element):

    _tag_type: str = "main"


class Map(Element):

    _tag_type: str = "map"


class Mark(Element):

    _tag_type: str = "mark"


class Meta(Element):

    _tag_type: str = "meta"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 name: str = None,
                 content: str = None,
                 http_equiv: str = None,
                 charset: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if name is not None:
            self.name = name

        if content is not None:
            self.content = content

        if http_equiv is not None:
            self.http_equiv = http_equiv

        if charset is not None:
            self.charset = charset

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def content(self) -> str:
        return self.get_attribute("content")

    @content.setter
    def content(self, value: str) -> None:
        self.set_attribute("content", value)

    @property
    def http_equiv(self) -> str:
        return self.get_attribute("http-equiv")

    @http_equiv.setter
    def http_equiv(self, value: str) -> None:
        self.set_attribute("http-equiv", value)

    @property
    def charset(self) -> str:
        return self.get_attribute("charset")

    @charset.setter
    def charset(self, value: str) -> None:
        self.set_attribute("charset", value)


class Meter(Element):

    _tag_type: str = "meter"


class Nav(Element):

    _tag_type: str = "nav"


class Noscript(Element):

    _tag_type: str = "noscript"


class Object(Element):

    _tag_type: str = "object"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 data: str = None,
                 type: str = None,
                 form_id: str = None,
                 width: str = None,
                 height: str = None,
                 usemap: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if data is not None:
            self.data = data

        if type is not None:
            self.type = type

        if form_id is not None:
            self.form_id = form_id

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

        if usemap is not None:
            self.usemap = usemap

    @property
    def data(self) -> str:
        return self.get_attribute("data")

    @data.setter
    def data(self, value: str) -> None:
        self.set_attribute("data", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

    @property
    def form_id(self) -> str:
        return self.get_attribute("form")

    @form_id.setter
    def form_id(self, value: str) -> None:
        self.set_attribute("form", value)

    @property
    def width(self) -> str:
        return self.get_attribute("width")

    @width.setter
    def width(self, value: str) -> None:
        self.set_attribute("width", value)

    @property
    def height(self) -> str:
        return self.get_attribute("height")

    @height.setter
    def height(self, value: str) -> None:
        self.set_attribute("height", value)

    @property
    def usemap(self) -> str:
        return self.get_attribute("usemap")

    @usemap.setter
    def usemap(self, value: str) -> None:
        self.set_attribute("usemap", value)


class Ol(Element):

    _tag_type: str = "ol"


class Optgroup(Element):

    _tag_type: str = "optgroup"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 label: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if label is not None:
            self.label = label

    @property
    def label(self) -> str:
        return self.get_attribute("label")

    @label.setter
    def label(self, value: str) -> None:
        self.set_attribute("label", value)


class Option(Element):

    _tag_type: str = "option"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 value: str = None,
                 selected: bool = False,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if value is not None:
            self.value = value

        if selected:
            self.selected = selected

    @property
    def value(self) -> str:
        return self.get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        self.set_attribute("value", value)

    @property
    def selected(self) -> bool:
        return self.get_attribute("selected")

    @selected.setter
    def selected(self, value: bool) -> None:
        self.set_attribute("selected", value)


class P(Element):

    _tag_type: str = "p"


class Param(Element):

    _tag_type: str = "param"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 name: str = None,
                 value: str = None,
                 type: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if name is not None:
            self.name = name

        if value is not None:
            self.value = value

        if type is not None:
            self.type = type

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def value(self) -> str:
        return self.get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        self.set_attribute("value", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)


class Picture(Element):

    _tag_type: str = "picture"


class Pre(Element):

    _tag_type: str = "pre"


class Progress(Element):

    _tag_type: str = "progress"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 value: str = None,
                 max: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if value is not None:
            self.value = value

        if max is not None:
            self.max = max

    @property
    def value(self) -> str:
        return self.get_attribute("value")

    @value.setter
    def value(self, value: str) -> None:
        self.set_attribute("value", value)

    @property
    def max(self) -> str:
        return self.get_attribute("max")

    @max.setter
    def max(self, value: str) -> None:
        self.set_attribute("max", value)


class Q(Element):

    _tag_type: str = "q"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 cite: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if cite is not None:
            self.cite = cite

    @property
    def cite(self) -> str:
        return self.get_attribute("cite")

    @cite.setter
    def cite(self, value: str) -> None:
        self.set_attribute("cite", value)


class Rp(Element):

    _tag_type: str = "rp"


class Rt(Element):

    _tag_type: str = "rt"

class Ruby(Element):

    _tag_type: str = "ruby"

class S(Element):

    _tag_type: str = "s"

class Samp(Element):

    _tag_type: str = "samp"

class Script(Element):

    _tag_type: str = "script"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 src: str = None,
                 type: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if src is not None:
            self.src = src

        if type is not None:
            self.type = type

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

class Section(Element):

    _tag_type: str = "section"

class Select(Element):

    _tag_type: str = "select"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 name: str = None,
                 size: str = None,
                 form_id: str = None,
                 multiple: bool = False,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if name is not None:
            self.name = name

        if size is not None:
            self.size = size
        
        if form_id is not None:
            self.form_id = form_id

        if multiple:
            self.multiple = multiple

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def size(self) -> str:
        return self.get_attribute("size")

    @size.setter
    def size(self, value: str) -> None:
        self.set_attribute("size", value)

    @property
    def multiple(self) -> bool:
        return self.get_attribute("multiple")

    @multiple.setter
    def multiple(self, value: bool) -> None:
        self.set_attribute("multiple", value)
    
    @property
    def form_id(self) -> str:
        return self.get_attribute("form")
    
    @form_id.setter
    def form_id(self, value: str) -> None:
        self.set_attribute("form", value)

class Small(Element):

    _tag_type: str = "small"

class Source(Element):

    _tag_type: str = "source"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 src: str = None,
                 type: str = None,
                 media: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if src is not None:
            self.src = src

        if type is not None:
            self.type = type

        if media is not None:
            self.media = media

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

    @property
    def media(self) -> str:
        return self.get_attribute("media")

    @media.setter
    def media(self, value: str) -> None:
        self.set_attribute("media", value)

class Span(Element):

    _tag_type: str = "span"

class Strong(Element):

    _tag_type: str = "strong"

class Style(Element):

    _tag_type: str = "style"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 media: str = None,
                 type: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if type is not None:
            self.type = type
    
        if media is not None:
            self.media = media
    
    @property
    def media(self) -> str:
        return self.get_attribute("media")
    
    @media.setter
    def media(self, value: str) -> None:
        self.set_attribute("media", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

class Sub(Element):

    _tag_type: str = "sub"

class Summary(Element):

    _tag_type: str = "summary"

class Sup(Element):

    _tag_type: str = "sup"

class Svg(Element):

    _tag_type: str = "svg"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 width: str = None,
                 height: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if width is not None:
            self.width = width

        if height is not None:
            self.height = height

    @property
    def width(self) -> str:
        return self.get_attribute("width")

    @width.setter
    def width(self, value: str) -> None:
        self.set_attribute("width", value)

    @property
    def height(self) -> str:
        return self.get_attribute("height")

    @height.setter
    def height(self, value: str) -> None:
        self.set_attribute("height", value)

class Table(Element):
    
    _tag_type: str = "table"

class TBody(Element):

    _tag_type: str = "tbody"

class Td(Element):

    _tag_type: str = "td"

class Template(Element):

    _tag_type: str = "template"

class TextArea(Element):

    _tag_type: str = "textarea"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 name: str = None,
                 cols: str = None,
                 rows: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if name is not None:
            self.name = name

        if cols is not None:
            self.cols = cols

        if rows is not None:
            self.rows = rows

    @property
    def name(self) -> str:
        return self.get_attribute("name")

    @name.setter
    def name(self, value: str) -> None:
        self.set_attribute("name", value)

    @property
    def cols(self) -> str:
        return self.get_attribute("cols")

    @cols.setter
    def cols(self, value: str) -> None:
        self.set_attribute("cols", value)

    @property
    def rows(self) -> str:
        return self.get_attribute("rows")

    @rows.setter
    def rows(self, value: str) -> None:
        self.set_attribute("rows", value)

class TFoot(Element):

    _tag_type: str = "tfoot"

class Th(Element):

    _tag_type: str = "th"

class THead(Element):

    _tag_type: str = "thead"

class Time(Element):

    _tag_type: str = "time"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: Element = None,
                 datetime: str = None,
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        if datetime is not None:
            self.datetime = datetime

    @property
    def datetime(self) -> str:
        return self.get_attribute("datetime")

    @datetime.setter
    def datetime(self, value: str) -> None:
        self.set_attribute("datetime", value)

class Title(Element):

    _tag_type: str = "title"

class Tr(Element):

    _tag_type: str = "tr"

class Track(Element):

    _tag_type: str = "track"

    def __init__(self,
                    id: str = None,
                    class_name: str = None,
                    parent: Element = None,
                    src: str = None,
                    src_lang: str = None,
                    label: str = None,
                    kind: str = None,
                    default: str = None,
                    inner_html: str = None) -> None:
            super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)
    
            if src is not None:
                self.src = src
    
            if src_lang is not None:
                self.src_lang = src_lang
    
            if label is not None:
                self.label = label
            
            if kind is not None:
                self.kind = kind
    
            if default is not None:
                self.default = default
    
    @property
    def src(self) -> str:
        return self.get_attribute("src")
    
    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)
    
    @property
    def src_lang(self) -> str:
        return self.get_attribute("src-lang")
    
    @src_lang.setter
    def src_lang(self, value: str) -> None:
        self.set_attribute("src-lang", value)
    
    @property
    def label(self) -> str:
        return self.get_attribute("label")
    
    @label.setter
    def label(self, value: str) -> None:
        self.set_attribute("label", value)
    
    @property
    def kind(self) -> str:
        return self.get_attribute("kind")
    
    @kind.setter
    def kind(self, value: str) -> None:
        self.set_attribute("kind", value)
    
    @property
    def default(self) -> str:
        return self.get_attribute("default")
    
    @default.setter
    def default(self, value: str) -> None:
        self.set_attribute("default", value)


class U(Element):

    _tag_type: str = "u"

class Ul(Element):

    _tag_type: str = "ul"

class Var(Element):

    _tag_type: str = "var"



class Video(Element):

    _tag_type: str = "video"

    def __init__(self,
                 id: str = None,
                 class_name: str = None,
                 parent: "Element" = None,
                 autoplay: bool = False,
                 controls: bool = False,
                 height: str = None,
                 width: str = None,
                 muted: bool = False,
                 poster: str = None,
                 preload: str = None,
                 src: str = None,
                 type: str = "video/mp4",
                 inner_html: str = None) -> None:
        super().__init__(id=id, class_name=class_name, parent=parent, inner_html=inner_html)

        self.type = type
        self.autoplay = autoplay
        self.controls = controls

        if height is not None:
            self.height = height

        if width is not None:
            self.width = width

        if muted is not None:
            self.muted = muted

        if poster is not None:
            self.poster = poster

        if preload is not None:
            self.preload = preload

        if src is not None:
            self.src = src

    @property
    def autoplay(self) -> bool:
        return self.get_attribute("autoplay", is_boolean_attribute=True)

    @autoplay.setter
    def autoplay(self, value: bool) -> None:
        self.set_attribute("autoplay", value, is_boolean_attribute=True)

    @property
    def controls(self) -> bool:
        return self.get_attribute("controls", is_boolean_attribute=True)

    @controls.setter
    def controls(self, value: bool) -> None:
        self.set_attribute("controls", value, is_boolean_attribute=True)

    @property
    def muted(self) -> bool:
        return self.get_attribute("muted", is_boolean_attribute=True)

    @muted.setter
    def muted(self, value: bool) -> None:
        self.set_attribute("muted", value, is_boolean_attribute=True)

    @property
    def poster(self) -> str:
        return self.get_attribute("poster")

    @poster.setter
    def poster(self, value: str) -> None:
        self.set_attribute("poster", value)

    @property
    def preload(self) -> str:
        return self.get_attribute("preload")

    @preload.setter
    def preload(self, value: str) -> None:
        self.set_attribute("preload", value)

    @property
    def src(self) -> str:
        return self.get_attribute("src")

    @src.setter
    def src(self, value: str) -> None:
        self.set_attribute("src", value)

    @property
    def type(self) -> str:
        return self.get_attribute("type")

    @type.setter
    def type(self, value: str) -> None:
        self.set_attribute("type", value)

class Wbr(Element):

    _tag_type: str = "wbr"
