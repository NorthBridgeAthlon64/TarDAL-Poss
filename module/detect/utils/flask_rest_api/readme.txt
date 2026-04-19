Flask REST API
==============

REST APIs are commonly used to expose machine learning models to other services. This folder contains an example REST API
created using Flask to expose the YOLOv5s model from PyTorch Hub: https://pytorch.org/hub/ultralytics_yolov5/

Requirements
------------
Flask is required. Install with:

  pip install Flask

Run
---
After Flask installation run:

  python3 restapi.py --port 5000

Then use curl to perform a request:

  curl -X POST -F image=@zidane.jpg "http://localhost:5000/v1/object-detection/yolov5s"

The model inference results are returned as a JSON response, for example (illustrative):

  [
    {
      "class": 0,
      "confidence": 0.8900438547,
      "height": 0.9318675399,
      "name": "person",
      "width": 0.3264600933,
      "xcenter": 0.7438579798,
      "ycenter": 0.5207948685
    }
  ]

An example python script to perform inference using requests is given in example_request.py
  (https://docs.python-requests.org/en/master/)
