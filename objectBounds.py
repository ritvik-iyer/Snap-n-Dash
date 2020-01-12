from google.cloud import vision
from google.cloud.vision import types
import io
import os
import math
import random

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getcwd() + r"\private-key.json"


def parse_image_details(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations
    object_details = []
    for object in objects:
        object_name = object.name
        object_score = object.score
        vertex_set = [(vertex.x, vertex.y) for vertex in object.bounding_poly.normalized_vertices]
        detail = (object_name, object_score, vertex_set)
        object_details.append(detail)
    return object_details

def topCoords(object_details):
    vertices = [object_detail[2] for object_detail in object_details]
    all_top_Coords = []
    for vertex_set in vertices:
        y_vals = []
        for point in vertex_set:
            y_vals.append(point[1])
        min_Y = min(y_vals)
        x_vals = []
        for point in vertex_set:
            if math.isclose(point[1], min_Y, rel_tol=1e-5):
                x_vals.append(point[0])
        x_vals.sort()
        topCoordinates = [x_vals[0], min_Y, x_vals[1], min_Y]
        all_top_Coords.append(topCoordinates)
    total = []
    for item in all_top_Coords:
        for subitem in item:
            total.append(subitem)
    challenge = []
    while len(challenge) != 4:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if  (((x**2) + (y**2))**(0.5) <= 0.3) and (((x**2) + (y**2))**(0.5) >= 0.05):
            challenge.extend([x, y])
    return total + challenge

if __name__ == '__main__':
    obj_dets = parse_image_details('test-images/test1.jpg')
    print(topCoords(obj_dets))
