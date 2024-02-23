# %%
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
import matplotlib.pyplot as plt


def predict_image(imagefile):
    # %%
    model = load_model("weights.hdf5")
    model.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=["accuracy"])

    # %%
    img = image.load_img(imagefile, target_size=(150, 150))
    imgplot = plt.imshow(img)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    predictions = model.predict(images, batch_size=10)
    classes = np.argmax(predictions, axis=1)

    if classes == [1]:
        print("Cancer")
    else:
        print("Normal")
