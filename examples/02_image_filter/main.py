from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import bootstrap_inputs as bInputs
from pyscript_bootstrap_templates import HTML as HTML


import numpy as np
from PIL import Image
from io import BytesIO
import cv2

# create a sobel image with OpenCV
def sobel_image(img):
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
    img_sobel = cv2.sqrt(cv2.addWeighted(cv2.pow(grad_x, 2.0), 0.5, cv2.pow(grad_y, 2.0), 0.5, 0))
    img_sobel = cv2.normalize(img_sobel, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    return img_sobel

# create a gaussian blur image with OpenCV
def gaussian_image(img):
    return cv2.GaussianBlur(img, (51, 51), 0)

# create a canny edge image with OpenCV
def canny_image(img):
    return cv2.Canny(img, 50, 100)

# convert to grayscale
def grayscale_image(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


app = bootstrap_templates.PyScriptBootstrapDashboard(parent_element="pyscript_app", brand_name="Image Filter Example")

filter_map = {
    "sobel": sobel_image,
    "gaussian": gaussian_image,
    "canny": canny_image,
    "grayscale": grayscale_image
}

filter_selection = bInputs.InputSelect(label_text="filter", parent=app.sidebar, options=list(filter_map.keys()) )

image_input = bInputs.InputFile(label_text="choose image file", parent=app.sidebar)
image_input._input.set_attribute("accept", "image/*")

process_button = bInputs.ButtonPrimary("process", parent=app.sidebar)
process_button.width = "100%"
process_button.m = 2





def on_process(*args, **kwargs):

    for child in app.main.children.copy():
        app.main.remove_child(child)
        child.destroy()

    file_dictionary = image_input.value
    if len(file_dictionary) == 0:
        app.alert_danger(message="no image selected")
        return
    
    # get first file
    name, f = list(file_dictionary.items())[0]

    f.seek(0)
    img = Image.open(f)
    img = np.array(img)

    filter_name = filter_selection.value

    img = filter_map[filter_name](img)

    bHTML.HTML.H3(f"{name} ({img.shape[0]}x{img.shape[1]}):", parent=app.main)

    output = bHTML.Image.from_numpy_array(img, parent=app.main)
    output.rounded = True
    output.rounded_size = 10
    output.width = "100%"
    output.shadow = bHTML.Shadow.LARGE


    app.toast(message="processing done", title="Info")


process_button.onclick = on_process

# alternatively, you can register the callback function with the file input element:
#image_input.onchange = on_image_change
