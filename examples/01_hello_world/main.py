
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import HTML as HTML

app = bootstrap_templates.PyScriptBootstrapDashboard(
    parent_element="pyscript_app", brand_name="hello_world")


div = bHTML.Div("This is a sidebar", parent=app.sidebar)
div.font_size = 4

btn = bHTML.ButtonPrimary("Click me", parent=app.sidebar)
btn.w = 100

toast_container = bHTML.ToastContainer(parent=app.main)
toast_container.position_bottom = 0
toast_container.position_end = 0



def onclick(_):
    alert = bHTML.AlertSuccess("You clicked me!", parent=app.main)
    alert.w = 25
    toast = bHTML.Toast("You clicked me!", parent=toast_container)
    toast.animation = True
    toast.show()

btn.onclick = onclick
    