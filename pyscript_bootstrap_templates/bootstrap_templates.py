from . import HTML
from . import bootstrap_HTML as bHTML
from js import document # type: ignore

class PyScriptBootstrapApp(object):
    def __init__(self, parent_element:str = "pyscript_app"):
        self._main_div = bHTML.ContainerFluid(id="main")

        self._main_div.w = 100
        self._main_div.vh_100 = True

        self._main_div.p = 0
        self._main_div.m = 0

        self._main_div.col_xs = 12
        self._main_div.col = 12



        self._parent_element = document.getElementById(parent_element)
        self._parent_element.appendChild(self._main_div.element)

        self._toast_container = bHTML.ToastContainer(parent=self._main_div)
        self._toast_container.position_end = 0
        self._toast_container.position_bottom = 0

        self._alert_container = bHTML.BootstrapContainer(parent=self._main_div)
        self._alert_container.position_end = 0
        self._alert_container.position_bottom = 0
        self._alert_container.position = bHTML.Position.ABSOLUTE
    
    def _alert(self, message: str, alert_class: type):
        return alert_class(message, parent=self._alert_container)
        bHTML.Al

    @property
    def main(self) -> HTML.Div:
        return self._main_div
    
    @property
    def toast_container(self) -> bHTML.ToastContainer:
        return self._toast_container
    
    @property
    def alert_container(self) -> bHTML.BootstrapContainer:
        return self._alert_container
    
    def toast(self, message: str, title: str, animation: bool = True, show: bool = True) -> bHTML.Toast:
        """
        show a toast on the default toast location (bottom right)
        """
        toast = bHTML.Toast(inner_html=message, title=title, parent=self._toast_container)
        toast.animation = animation
        if show:
            toast.show()
        return toast
    
    def alert(self, message:str) -> bHTML.Alert:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.Alert)
    
    def alert_success(self, message:str) -> bHTML.AlertSuccess:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertSuccess)
    
    def alert_info(self, message:str) -> bHTML.AlertInfo:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertInfo)

    def alert_warning(self, message:str) -> bHTML.AlertWarning:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertWarning)
    
    def alert_danger(self, message:str) -> bHTML.AlertDanger:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertDanger)

    def alert_primary(self, message:str) -> bHTML.AlertPrimary:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertPrimary)

    def alert_secondary(self, message:str) -> bHTML.AlertSecondary:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertSecondary)

    def alert_light(self, message:str) -> bHTML.AlertLight:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertLight)
    
    def alert_dark(self, message:str) -> bHTML.AlertDark:
        """
        show an alert on the default alert location (bottom right)
        """
        return self._alert(message, bHTML.AlertDark)

class PyScriptBootstrapDashboard(PyScriptBootstrapApp):
    def __init__(self, parent_element:str = "pyscript_app", brand_name = "Dashboard"):

        super().__init__(parent_element)

        self._sidebar = bHTML.Col(id="sidebar", col=12, col_sm=12, col_md=4, col_lg=3, col_xl=3)
        self._sidebar.style = {"height": "100vh", "overflow": "auto"}

        self._navbar = bHTML.NavbarDark(
            parent=self._main_div,
            brand = brand_name,
            nav_fill=True,
            toggle_button_for_target=self.sidebar
        )

        self._navbar.position = bHTML.Position.FIXED_TOP
        self._navbar.height = "4em"
        self._navbar.ps = 5
        self._navbar.pe = 5
        self._navbar.col = 12

        
        top_margin_dummy = bHTML.BootstrapContainer(id="top_margin_dummy", parent=self._main_div)
        top_margin_dummy.height = "3.5em" # have it slightly less high than navbar
        top_margin_dummy.width = "100vw"
        top_margin_dummy.m = 0
        top_margin_dummy.p = 0


        row = bHTML.Row(parent=self._main_div)
        row.w = 100

        row.height = "calc(100vh - 4em)"
        row.p = 0
        row.m = 0
        row.col_xs = 12
        row.col = 12


        row.display_property = bHTML.DisplayProperty.INLINE_FLEX

        row.append_child(self.sidebar)
        self._sidebar.add_classes("sidebar")
        self._sidebar.background_color = bHTML.BackgroundColor.LIGHT
        self._sidebar.p = 4
        self._sidebar.g = 2
        self._sidebar.position = bHTML.Position.STATIC
        self._sidebar.collapsable = True
        self._sidebar.mw = 100
        self._sidebar.height = "calc(100vh - 4em)"
        self._sidebar.shadow = bHTML.Shadow.LARGE
        self._sidebar.overflow = bHTML.Overflow.SCROLL
        


        self._modal = bHTML.Modal(parent=self._main_div, title="Modal")

        self._main_area = bHTML.Col(id="main_area", parent=row, col=12, col_sm=12, col_md=8, col_lg=9, col_xl=9)
        
        self._main_area.p = 4
        self._main_area.overflow = bHTML.Overflow.SCROLL
        self._main_area.height = "calc(100vh - 4em)"
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
