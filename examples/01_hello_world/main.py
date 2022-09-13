
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import HTML as HTML

app = bootstrap_templates.PyScriptBootstrapDashboard(
    parent_element="pyscript_app", brand_name="hello_world")
div = bHTML.BootstrapContainer("This is a sidebar", parent=app.sidebar)
div.font_size = 4

btn = bHTML.ButtonPrimary("Click me", parent=app.sidebar)
btn.w = 100

def onclick(_):
    alert = bHTML.AlertSuccess("You clicked me!", parent=app.main_area)
    toast = bHTML.Toast("You clicked me!", parent=app.main_area)
    toast.position_bottom = 0
    toast.position_end = 0
    toast.show()

btn.onclick = onclick
    