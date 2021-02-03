from flask import Flask, request, abort
import urllib
import numpy as np
import cv2
import easyocr
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'easyocr_vdt');
reader = easyocr.Reader(['en'], gpu=False)

app = Flask(__name__)


def url_to_image(url):
    """
    download the image, convert it to a NumPy array, and then read it into OpenCV format
    :param url: url to the image
    :return: image in format of Opencv
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    print("url = ", url)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def data_process(data):
    """
    read params from the received data
    :param data: in json format
    :return: params for image processing
    """
    image_url = data["image_url"]
    secret_key = data["secret_key"]

    return url_to_image(image_url), secret_key


def recognition(image):
    """

    :param image:
    :return:
    """
    results = []
    texts = reader.readtext(image)
    for (bbox, text, prob) in texts:
        output = {
            "coordinate": [list(map(float, coordinate)) for coordinate in bbox],
            "text": text,
            "score": prob
        }
        results.append(output)

    return results


@app.route('/ocr', methods=['GET', 'POST'])
def process():
    """
    received request from client and process the image
    :return: dict of width and points
    """
    data = request.get_json()
    image, secret_key = data_process(data)
    if secret_key == SECRET_KEY:
        results = recognition(image)
        return {
            "results": results
        }
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2000)
