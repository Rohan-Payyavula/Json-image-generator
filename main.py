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

def get_color_map(names):
    unique_names = list(set(names))
    color_map = plt.get_cmap('tab10', len(unique_names))  
    name_to_color = {name: color_map(i) for i, name in enumerate(unique_names)}
    return name_to_color

def visualize_with_matplotlib(image_path, annotations, output_path):
    image = Image.open(image_path)
    plt.figure(figsize=(8, 8))
    plt.imshow(image)

    names = [region["region_attributes"]["name"] for region in annotations["regions"] if
             "name" in region["region_attributes"]]
    name_to_color = get_color_map(names)

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

            ellipse = Ellipse((cx, cy), 2 * rx, 2 * ry, angle=theta_deg, edgecolor='r', facecolor='none', lw=2)
            plt.gca().add_patch(ellipse)

            if "name" in region_attr:
                text = region_attr["name"]
                color = name_to_color[text]
                plt.text(cx, cy + ry + 30, text, color=color, fontsize=8, ha='center')

    plt.axis('off')

    plt.savefig(output_path, bbox_inches='tight', pad_inches=0, format='png')
    plt.close()

def process_all_images_in_directory(json_path, images_directory, output_directory):
    json_output = load_labelme_annotations(json_path)

    for key in json_output.keys():
        image_filename = json_output[key]['filename']
        image_path = os.path.join(images_directory, image_filename)
        output_path = os.path.join(output_directory, 'annotated_matplotlib_' + os.path.splitext(image_filename)[0] + '.png')

        visualize_with_matplotlib(image_path, json_output[key], output_path)

json_path = '/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/Keratoplasty _json.json'
images_directory = '/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/images'
output_directory = '/Users/rohanpayyavula/Desktop/Keratoplasty Clear Graft Set 1/Output'

process_all_images_in_directory(json_path, images_directory, output_directory)
