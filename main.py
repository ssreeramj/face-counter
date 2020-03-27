import os

import boto3
import cv2
from PIL import Image

from credentials import ACCESS_ID, SECRET_KEY

os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
IMG_DIR = os.path.join(os.getcwd(), 'static/img')
OUT_FILE = os.path.join(IMG_DIR, 'output_image.jpg')

client = boto3.client('rekognition', aws_access_key_id=ACCESS_ID, aws_secret_access_key= SECRET_KEY)

def get_bbox(x, y, w, h, img):
    img_width, img_height = Image.open(os.path.join(IMG_DIR, img)).size
    left, top, width, height = int(img_width * x), int(img_height * y), int(img_width * w), int(img_height * h)
    
    return left, top, width, height

def get_faces(img):
    with open(os.path.join(IMG_DIR, img), 'rb') as test_image:

        response = client.detect_faces(Image={'Bytes': test_image.read()})
        output_image = cv2.imread(os.path.join(IMG_DIR, img),)

    # response is a dictionary, we require 'FaceDetails' attribute
        face_details = response['FaceDetails']

        for face in face_details:
            bbox_ratio = face['BoundingBox']
            left, top, width, height = get_bbox(
                bbox_ratio['Left'], bbox_ratio['Top'], bbox_ratio['Width'], bbox_ratio['Height'], img)

            cv2.rectangle(output_image, (left, top), (left+width, top+height), (0, 0, 255), 2)

        
        cv2.imwrite(os.path.join(IMG_DIR, f'res_{img}'), output_image)

        return len(face_details)

# print(get_faces('my_photo.jpg'))


