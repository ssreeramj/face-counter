import os
import json

import boto3
import cv2
from PIL import Image

from credentials import ACCESS_ID, SECRET_KEY

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
IMG_DIR = os.path.join(os.getcwd(), 'images/')
IMG_FILE = os.path.join(IMG_DIR, 'test_image2.png')

client = boto3.client('rekognition', aws_access_key_id=ACCESS_ID, aws_secret_access_key= SECRET_KEY)
sample_image = cv2.imread(IMG_FILE,)

def get_bbox(x, y, w, h, img):
    img_width, img_height = Image.open(img).size
    left, top, width, height = int(img_width * x), int(img_height * y), int(img_width * w), int(img_height * h)
    
    return left, top, width, height


with open(IMG_FILE, 'rb') as test_image:

    response = client.detect_faces(Image={'Bytes': test_image.read()})

# response is a dictionary, we require 'FaceDetails' attribute
    face_details = response['FaceDetails']

    for face in face_details:
        bbox_ratio = face['BoundingBox']
        left, top, width, height = get_bbox(
            bbox_ratio['Left'], bbox_ratio['Top'], bbox_ratio['Width'], bbox_ratio['Height'], IMG_FILE)

        cv2.rectangle(sample_image, (left, top), (left+width, top+height), (255, 0, 0), 1)


    cv2.imshow('Image', sample_image)   
    cv2.waitKey(0)

    cv2.destroyAllWindows()


