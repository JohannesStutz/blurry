# Blurry
> A tool to increase privacy when sharing photos. It detects faces and blurs them.


Readme will follow as project makes progress.

## Install

There is no install available at the moment. If you want to play around with the code, just download the Jupyter notebooks. Requirements: `opencv-python`, `PIL`.

## How to use

At the moment Blurry can be used to blur faces in single photos.

```python
img = load_img('test_images/group_closer.jpg')
result = anonymize(img, factor=1.5, mode='pixelate')
show_cv2(result)
```

To play with live video from webcam, go to the 01_webcam.ipynb notebook.

## To Do
- Command line tool to process photos
- More options (pixelate/blur)
- Improve aesthetics
- A way to manually blur parts of the image
- Detect and blur text
