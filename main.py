import json
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image

def load_labelme_annotations(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data

def visualize_with_matplotlib(image_path, annotations, output_path):

    image = Image.open(image_path)
    plt.figure(figsize=(8, 8))
    plt.imshow(image)

    for each_region in annotations["regions"]:
        shape_attr = each_region["shape_attributes"]
        region_attr = each_region["region_attributes"]
        if shape_attr["name"] == "ellipse":
            cx = shape_attr["cx"]
            cy = shape_attr["cy"]
            rx = shape_attr["rx"]
            ry = shape_attr["ry"]
            theta = shape_attr["theta"]

            theta_deg = np.degrees(theta)

            ellipse = Ellipse((cx, cy), 2*rx, 2*ry, angle=theta_deg, edgecolor='r', facecolor='none', lw=2)
            plt.gca().add_patch(ellipse)

            if "name" in region_attr:
                text = region_attr["name"]
                plt.text(cx, cy + ry + 30, text, color='blue', fontsize=12, ha='center')

    plt.axis('off')
    plt.show()

    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)

json_path = '/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/Keratoplasty _json.json'
json_output = load_labelme_annotations(json_path)

first_key = list(json_output.keys())[0]
image_filename = json_output[first_key]['filename']
image_path = os.path.join("/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/", image_filename)

output_path = os.path.join("/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/", 'annotated_matplotlib_' + image_filename)

visualize_with_matplotlib(image_path, json_output[first_key], output_path)
