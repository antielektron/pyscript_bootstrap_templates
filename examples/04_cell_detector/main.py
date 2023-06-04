
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import bootstrap_inputs as bInputs
from pyscript_bootstrap_templates import HTML as HTML


import numpy as np
from PIL import Image
import cv2

loaded_img:np.ndarray = None

app = bootstrap_templates.PyScriptBootstrapDashboard(parent_element="pyscript_app", brand_name="Pyscript Cell Colony Detector")

main_div = bHTML.BootstrapContainer(parent=app.main)
main_div.w = 100
result_div = bHTML.BootstrapContainer (parent=main_div)


def process_image(image,
                  hough_min_dist = 500,
                  hough_param1 = 80,
                  hough_param2 = 500,
                  minRadius = 100,
                  maxRadius=500,
                  inner_hough_param1 = 25,
                  inner_hough_param2 = 50,
                  inner_hough_circles=True,
                  cell_colony_color_channel:int = None):
    
    for child in result_div.children:
        child.destroy()

    # Convert the image to grayscale
    if cell_colony_color_channel is None:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.astype(float)[...,cell_colony_color_channel]
        gray = (255 * gray / gray.max()).astype(np.uint8)

    # Use median blur to reduce noise
    gray = cv2.medianBlur(gray, 5)

    # Apply Hough transform on the image to find circles
    circles = cv2.HoughCircles(gray,
                               cv2.HOUGH_GRADIENT,
                               2,
                               minDist=hough_min_dist,
                               param1=hough_param1,
                               param2=hough_param2,
                               minRadius=minRadius,
                               maxRadius=maxRadius)

    if circles is None:
        app.alert_danger("No cell areas detected in image")
        return False
    
    # Convert to integers
    circles = np.uint16(np.around(circles))

    # Loop over all detected circles and add them to the image
    #for i in circles[0,:]:
    #    # Draw outer circle
    #    cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
    #    # Draw center of circle
    #    cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)

    first_wells = []
    first_wells_gray = []


    for i in circles[0,:]:
        
        center = (i[0], i[1])
        radius = i[2]
        

        # Cut out the well
        well = image[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]
        well_gray = gray[center[1]-radius:center[1]+radius, center[0]-radius:center[0]+radius]
        

        first_wells.append(well)
        first_wells_gray.append(well_gray)

    if inner_hough_circles:

        second_wells = []
        second_wells_gray = []

        for well, well_gray in zip(first_wells, first_wells_gray):
            
            circles = cv2.HoughCircles(well_gray,
                                       cv2.HOUGH_GRADIENT,
                                       1,
                                       minDist=hough_min_dist,
                                       param1=inner_hough_param1,
                                       param2=inner_hough_param2,
                                       minRadius=int((min(well.shape[0],well.shape[1]) // 2)*0.79),
                                       maxRadius=int((min(well.shape[0],well.shape[1]) // 2)*0.95))
            if circles is not None:
                circles = np.uint16(np.around(circles))
                i = circles[0,:][0]
                center = (i[0], i[1])
                radius = i[2] - 1
                
                min_y = max(center[1]-radius, 0)
                max_y = center[1]+radius
                
                min_x = max(center[0]-radius, 0)
                max_x = center[0]+radius
                

                
                second_wells.append(well[min_y:max_y, min_x:max_x])
                second_wells_gray.append(well_gray[min_y:max_y, min_x:max_x])    
            else:
                second_wells.append(well)
                second_wells_gray.append(well_gray)
        
    else:
        second_wells = first_wells
        second_wells_gray = first_wells_gray
    
    tabs = {}

    for well in second_wells:
        
        well_gray = cv2.cvtColor(well, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(255 - well_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    

        # Perform some morphological operations to remove small noise - you can change the kernel size
        kernel = np.ones((3,3),np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        

        radius = min(well.shape[0], well.shape[1]) // 2 -1
        # Now clear all pixels outside the circular well.
        # We do this by creating a mask for the well and applying it to the image.
        well_mask = np.zeros_like(cleaned, dtype=np.uint8)
        cv2.circle(well_mask, (well.shape[1] // 2, well.shape[0] // 2), radius, 1, thickness=-1)
        cleaned = cleaned * well_mask

        circle = well_mask > 0

        # now create an image overlay to display
        ratio = np.sum((cleaned > 0).astype(int)) / np.sum(circle.astype(int))
        div_result = bHTML.BootstrapContainer(f"ratio: {ratio * 100}%")
        div_result.shadow = bHTML.Shadow.LARGE
        div_result.rounded = True
        div_result.w = 75
        div_result.h = 75
        div_result.rounded_size = 50
        div_result.p = 3

        well = well.copy()
        well[cleaned > 0,0] = 255
        final_img = bHTML.Image.from_numpy_array(well, parent=div_result)
        final_img.rounded = True
        final_img.rounded_size = 50
        final_img.shadow = bHTML.Shadow.LARGE
        final_img.w = 100

        tabs[f"Well #{len(tabs) + 1}"] = div_result
    
    tabs = bHTML.Tabs(tabs, parent=result_div)
    tabs.w = 100


div = bHTML.BootstrapContainer("Controls", parent=app.sidebar)
div.font_size = 4

image_input = bInputs.InputFile(label_text="choose image file", parent=app.sidebar)

btn = bHTML.ButtonPrimary("Process", parent=app.sidebar)
btn.w = 100
btn.mt = 3
btn.mb = 3
btn.ml = 4
btn.mr = 4

i_hough_min_dist = bInputs.InputInt("hough min distance [px]",
                                    parent=app.sidebar,
                                    help_text="minimal distance between wells in pixels")
i_hough_min_dist.value = 500

i_hough_param1 = bInputs.InputInt("hough param1",
                                  parent=app.sidebar,
                                  help_text="parameter for canny edge detector")
i_hough_param1.value = 80

i_hough_param2 = bInputs.InputInt("hough param2",
                                  parent=app.sidebar,
                                  help_text="increase this value to prevent false circle detection")
i_hough_param2.value = 500

i_hough_min_radius = bInputs.InputInt("hough min radius [px]",
                                       parent=app.sidebar,
                                       help_text="min radius for circle detection")
i_hough_min_radius.value = 100

i_hough_max_radius = bInputs.InputInt("hough max radius [px]",
                                       parent=app.sidebar,
                                       help_text="max radius for circle detection")
i_hough_max_radius.value = 500

i_inner_hough = bInputs.InputCheckboxSingle("nested hough transform?",
                                             parent=app.sidebar,
                                             help_text="if set, circle detection will be applied twice on detected wells")
i_inner_hough.value = True
i_inner_hough.m = 3

i_inner_hough_param1 = bInputs.InputInt("inner hough param1", parent=app.sidebar)
i_inner_hough_param1.value = 25

i_inner_hough_param2 = bInputs.InputInt("inner hough param2", parent=app.sidebar)
i_inner_hough_param2.value = 50

i_use_color_channel = bInputs.InputSelect(["all",
                                            "red",
                                            "green",
                                            "blue"],
                                            label_text="cell colony color channel",
                                            parent=app.sidebar,
                                            help_text="if cells are more present in a specific channel, select it here")
i_use_color_channel.value = "blue"





def on_image_change(f, *args):

    try:
        global loaded_img
        f.seek(0)
        img = np.array(Image.open(f))
        for child in result_div.children:
            child.destroy()

        bHTML.BootstrapContainer("input image:", parent=result_div)
        output = bHTML.Image.from_numpy_array(img, parent=result_div)
        output.rounded = True
        output.rounded_size = 10
        output.shadow = bHTML.Shadow.LARGE
        output.width = "100%"
        output.height = "100%"
        
        loaded_img = img

        app.toast("successfully loaded image", "info")
        #toast = bHTML.Toast("successfully loaded image", title="info", parent=toast_container)
        #toast.animation = True
        #toast.show()
    except Exception as e:
        for child in result_div.children:
            child.destroy()
        bHTML.AlertDanger(f"error while loading image: {str(e)}", parent=alert_container)


image_input.onchange = on_image_change    

def on_click(*args, **kwargs):
    if loaded_img is None:
        app.alert_danger("No image loaded")
        return
    for child in result_div.children:
        child.destroy()

    try:
        h_min_dist = int(i_hough_min_dist.value)
        h_param1 = int(i_hough_param1.value)
        h_param2 = int(i_hough_param2.value)
        h_inner_param1 = int(i_inner_hough_param1.value)
        h_inner_param2 = int(i_inner_hough_param2.value)
        h_min_radius = int(i_hough_min_radius.value)
        h_max_radius = int(i_hough_max_radius.value)
        inner_hough = bool(i_inner_hough.value)
        color_channel = {
            "all": None,
            "red": 0,
            "green": 1,
            "blue": 2
        }[i_use_color_channel.value]



        process_image(loaded_img,
                    hough_min_dist=h_min_dist,
                    hough_param1=h_param1,
                    hough_param2=h_param2,
                    minRadius=h_min_radius,
                    maxRadius=h_max_radius,
                    inner_hough_param1=h_inner_param1,
                    inner_hough_param2=h_inner_param2,
                    inner_hough_circles=inner_hough,
                    cell_colony_color_channel=color_channel)
        app.toast("successfully processed image", title="info")

    except Exception as e:
        for child in result_div.children:
            child.destroy()
        app.alert_danger(f"error while processing image: {str(e)}")

btn.onclick = on_click

    