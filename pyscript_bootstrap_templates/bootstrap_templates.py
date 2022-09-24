from . import HTML
from . import bootstrap_HTML as bHTML
from js import document # type: ignore

class PyScriptBootstrapApp(object):
    def __init__(self, parent_element:str = "pyscript_app"):
        self._main_div = bHTML.ContainerFluid(id="main")

        self._main_div.w = 100
        self._main_div.vh_100 = True

        self._main_div.p = 0

        self._parent_element = document.getElementById(parent_element)
        self._parent_element.appendChild(self._main_div.element)

    @property
    def main(self) -> HTML.Div:
        return self._main_div

class PyScriptBootstrapDashboard(PyScriptBootstrapApp):
    def __init__(self, parent_element:str = "pyscript_app", brand_name = "Dashboard"):

        super().__init__(parent_element)

        self._sidebar = bHTML.Col(id="sidebar", col_sm=5, col_md=4, col_lg=3, col_xl=3)

        self._navbar = bHTML.NavbarDark(
            parent=self._main_div,
            brand = brand_name,
            nav_fill=True,
            toggle_button_for_target=self.sidebar
        )

        self._navbar.position = bHTML.Position.STICKY_TOP
        self._navbar.w = 100


        row = bHTML.Row(parent=self._main_div)
        row.h = 100
        row.w = 100
        row.display_property = bHTML.DisplayProperty.INLINE_FLEX

        row.append_child(self.sidebar)
        self._sidebar.add_classes("sidebar")
        self._sidebar.background_color = bHTML.BackgroundColor.LIGHT
        self._sidebar.p = 4
        self._sidebar.g = 2
        self._sidebar.position = bHTML.Position.STATIC
        self._sidebar.collapsable = True
        self._sidebar.mw = 100
        self._sidebar.shadow = bHTML.Shadow.LARGE
        self._sidebar.overflow = bHTML.Overflow.HIDDEN
        


        self._modal = bHTML.Modal(parent=self._main_div, title="Modal")

        self._main_area = bHTML.Col(id="main_area", parent=row, col_lg=9, col_xl=9)
        self._main_area.p = 4
        self._main_area.overflow = bHTML.Overflow.HIDDEN
        #self._main_area.vh_100 = True
        self._main_area.mw = 100
    
    def show_modal(self):
        self.modal.show()
    
    def hide_modal(self):
        self.modal.hide()
    
    def toggle_modal(self):
        self.modal.toggle()

    
    @property
    def header(self) -> HTML.Header:
        return self._header
    
    @property
    def sidebar(self) -> HTML.Div:
        return self._sidebar
    
    @property
    def modal(self) -> HTML.Div:
        return self._modal
    
    @property
    def main(self) -> HTML.Div:
        return self._main_area
