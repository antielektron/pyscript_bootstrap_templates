

from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import bootstrap_inputs as bInputs
from pyscript_bootstrap_templates import HTML as HTML


import numpy as np
from PIL import Image
from io import BytesIO
from skimage import filters

# create a sobel image with skimage
def sobel_image(img):
    if len(img.shape) == 3:
        img = img[:,:,0] + img[:,:,1] + img[:,:,2]
        img = img / 3
    img_sobel = filters.sobel(img)
    return ((255 * img_sobel) / img_sobel.max()).astype(np.uint8)


app = bootstrap_templates.PyScriptBootstrapDashboard(parent_element="pyscript_app", brand_name="Sobel Filter Example")

HTML.H3("upload an image:", parent=app.sidebar)
HTML.H3("filtered image:", parent=app.main_area)



image_input = bInputs.InputFile(label_text="choose image file", parent=app.sidebar)
image_input._input.set_attribute("accept", "image/*") # TODO: write wrapper for this

def on_image_change(f, *args):
    print("image changed")
    print(f)
    f.seek(0)
    img = Image.open(f)
    img = sobel_image(np.array(img))

    output = bHTML.Image.from_numpy_array(img, parent=app.main_area)
    output.rounded = True
    output.rounded_size = 10
    output.shadow = bHTML.Shadow.LARGE

image_input.onchange = on_image_change

