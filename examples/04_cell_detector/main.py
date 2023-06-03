
from pyscript_bootstrap_templates import bootstrap_templates
from pyscript_bootstrap_templates import bootstrap_HTML as bHTML
from pyscript_bootstrap_templates import bootstrap_inputs as bInputs
from pyscript_bootstrap_templates import HTML as HTML


import numpy as np
from PIL import Image
import cv2

loaded_img = None

app = bootstrap_templates.PyScriptBootstrapDashboard(parent_element="pyscript_app", brand_name="Pyscript Cell Detector")

main_div = bHTML.BootstrapContainer(parent=app.main)
main_div.w = 100
result_div = bHTML.BootstrapContainer(parent=main_div)


def process_image(image,
                  hough_min_dist = 500,
                  hough_param1 = 80,
                  hough_param2 = 500,
                  minRadius = 100,
                  maxRadius=500,
                  inner_hough_circles=True):
    
    for child in result_div.children:
        child.destroy()
    #image = cv2.imread(str(test_img_path), cv2.IMREAD_COLOR)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        bHTML.AlertDanger("No cell areas detected in image", parent=app.main)
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
            
            circles = cv2.HoughCircles(well_gray, cv2.HOUGH_GRADIENT, 1, minDist=hough_min_dist, param1=50, param2=50, minRadius=(well.shape[0] // 2) - 50, maxRadius=(well.shape[0] // 2) - 10)
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
    

    for well, well_gray in zip(second_wells, second_wells_gray):
        
        _, binary = cv2.threshold(255 - well_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    

        # Perform some morphological operations to remove small noise - you can change the kernel size
        kernel = np.ones((3,3),np.uint8)
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        

        radius = well.shape[0] // 2 -1
        # Now clear all pixels outside the circular well.
        # We do this by creating a mask for the well and applying it to the image.
        well_mask = np.zeros_like(cleaned, dtype=np.uint8)
        cv2.circle(well_mask, (radius, radius), radius, 1, thickness=-1)
        cleaned = cleaned * well_mask

        circle = well_mask > 0

        # now create an image overlay to display
        ratio = np.sum((cleaned > 0).astype(int)) / np.sum(circle.astype(int))
        div_result = bHTML.BootstrapContainer(f"ratio: {ratio * 100}%", parent=result_div)
        div_result.shadow = bHTML.Shadow.LARGE
        div_result.rounded = True
        div_result.w = 50

        well[cleaned > 0,0] = 255
        final_img = bHTML.Image.from_numpy_array(well, parent=div_result)
        final_img.rounded = True
        final_img.rounded_size = 10
        final_img.shadow = bHTML.Shadow.LARGE
        final_img.w = 100



div = bHTML.BootstrapContainer("Controls", parent=app.sidebar)
div.font_size = 4

image_input = bInputs.InputFile(label_text="choose image file", parent=app.sidebar)

i_hough_min_dist = bInputs.InputInt("hough min distance [px]", parent=app.sidebar)
i_hough_min_dist.value = 500

i_hough_param1 = bInputs.InputInt("hough param1", parent=app.sidebar)
i_hough_param1.value = 80

i_hough_param2 = bInputs.InputInt("hough param2", parent=app.sidebar)
i_hough_param2.value = 500

i_hough_min_radius = bInputs.InputInt("hough min radius [px]", parent=app.sidebar)
i_hough_min_radius.value = 100

i_hough_max_radius = bInputs.InputInt("hough max radius [px]", parent=app.sidebar)
i_hough_max_radius.value = 500



btn = bHTML.ButtonPrimary("Process", parent=app.sidebar)
btn.w = 100



def on_image_change(f, *args):
    global loaded_img
    f.seek(0)
    img = np.array(Image.open(f))
    for child in result_div.children:
        child.destroy()
    
    output = bHTML.Image.from_numpy_array(img, parent=result_div)
    output.rounded = True
    output.rounded_size = 10
    output.shadow = bHTML.Shadow.LARGE
    output.w=50
    
    loaded_img = img

image_input.onchange = on_image_change    

def on_click(*args, **kwargs):
    if loaded_img is None:
        bHTML.AlertDanger("No image loaded", parent=app.main)
        return
    
    h_min_dist = int(i_hough_min_dist.value)
    h_param1 = int(i_hough_param1.value)
    h_param2 = int(i_hough_param2.value)
    h_min_radius = int(i_hough_min_radius.value)
    h_max_radius = int(i_hough_max_radius.value)


    process_image(loaded_img,
                  hough_min_dist=h_min_dist,
                  hough_param1=h_param1,
                  hough_param2=h_param2,
                  minRadius=h_min_radius,
                  maxRadius=h_max_radius,
                  inner_hough_circles=True)

btn.onclick = on_click

    