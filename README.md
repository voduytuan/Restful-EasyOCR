# Restful EasyOCR

If you do not know, EasyOCR is an open-sourced project (written in Python, hosted at https://github.com/JaidedAI/EasyOCR) helps doing OCR Jobs for your text extraction needs. Because it's written in Python, it can be difficult for integrating to your stack. 

This small repository helps wrapping the EasyOCR functionalities inside Restful API with Flask. So that, you do not need to use Python in your stack to work with EasyOCR.

## Run with default Docker Hub image

The fastest way to run is using provided image at https://hub.docker.com/voduytuan/restful-easyocr. 

### Start Docker Container

```shell
$ > docker run -d -i -p 2000:2000 -e SECRET_KEY=easyocr_vdt voduytuan/restful-easyocr
```

By default, this container will be accessed by port `2000`.

### HTTP Request:

- Method: `POST`

- URL: `http://{server-ip}:2000/ocr`

- Header: 

  - Content-Type: application/json

- Request Body:

  - JSON Object with format:

    - `image_url` - (String) : URL Of image will be processed
    - `secret_key` - (String): Secret Key of server. If you're using my public image from hub.docker.com, the secret key will be "easyocr_vdt". If you want to change key, build image yourself and change  in `recognition.py`.

  - Example of a payload:

    ```
    {
    	"secret_key": "easyocr_vdt",
    	"image_url": "https://via.placeholder.com/300.jpg?text=Hello_world"
    }
    ```

    *(Placeholder Image above has resolution 300x300px)*

### HTTP Response:
- Status Code: `200` (Success) or `401` if incorrect `secret_key`.

- Format: JSON

  - `results` (Array of Object): List of detected texts and rectangle boundary of that text on the source image. Each result object will have format:

    - `coordinate` (Array of Point): Contains 4 points to create rectangle contains the text. Each point is an two value array of float.
    - `score` (Float): The score of the easyocr when detect. From 0 (zero) to 1.
    - `text` (String): Detected text

  - An Example of response data: 

    ```json
    {
      "results": [
        {
          "coordinate": [
            [
              86.0,
              138.0
            ],
            [
              212.0,
              138.0
            ],
            [
              212.0,
              170.0
            ],
            [
              86.0,
              170.0
            ]
          ],
          "score": 0.24089430272579193,
          "text": "Hello world"
        }
      ]
    }
    ```

    

## Build your own docker image

By default, provided image is only detect ENGLISH text on input photo. If you want to change the language to detect, you can clone my repository (https://github.com/voduytuan/Restful-EasyOCR), then edit file `recognition.py` (in line number 9), you can change the array of detected languages by replacing the `['en']` array with your language array, such as `['vi', 'en']` (`EasyOCR` supports detect multiple language)

To know all the supported languages, you can view the repository EasyOCR (https://github.com/JaidedAI/EasyOCR) or access URL https://github.com/JaidedAI/EasyOCR/tree/master/easyocr/character to see full list, remove the suffix "`_char.txt`" from file names, you will have the name of language to set to your array. Such as: `vi_char.txt` becomes `vi`...

```bash
$ git clone https://github.com/voduytuan/Restful-EasyOCR
$ cd Restful-EasyOCR/

(Now, you can edit file recognition.py with your needs)
$ vi recognition.py

(save file and start building your image)
$ sudo docker build -t myrestful_easyocr -f Dockerfile .
```

### Run your own image

```bash
$ sudo docker run -d -i -e SECRET_KEY=easyocr_vdt -p 2000:2000 myrestful_easyocr
```
