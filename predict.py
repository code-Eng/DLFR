'''
This code take the image by parse argument and make prediction.
below how to run the code

python predict.py
-m 'output/simple_nn1.model'
-l 'output/simple_nn_lb1.pickle'
-w 32 -e 32 -f 1
-i 'test_images/arabic.jpg'

'''
# import the necessary packages
from keras.models import load_model
import argparse
import pickle
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image we are going to classify")
ap.add_argument("-m", "--model", required=True,
                help="path to trained Keras model")
ap.add_argument("-l", "--label-bin", required=True,
                help="path to label binarizer")
ap.add_argument("-w", "--width", type=int, default=28,
                help="target spatial dimension width")
ap.add_argument("-e", "--height", type=int, default=28,
                help="target spatial dimension height")
ap.add_argument("-f", "--flatten", type=int, default=-1,
                help="whether or not we should flatten the image")
args = vars(ap.parse_args())

# load the input image and resize it to the target spatial dimensions
image = cv2.imread(args["image"])
output = image.copy()
image = cv2.resize(image, (args["width"], args["height"]))

# check to see if we should flatten the image and add a batch
# dimension
if args["flatten"] > 0:
    image = image.flatten()
    image = image.reshape((1, image.shape[0]))

# otherwise, we must be working with a CNN -- don't flatten the
# image, simply add the batch dimension
else:
    image = image.reshape((1, image.shape[0], image.shape[1],
                           image.shape[2]))

# load the model and label binarizer
print('-'*90)
print("[INFO] loading network and label binarizer...")
print('-'*90)

model = load_model(args["model"])
lb = pickle.loads(open(args["label_bin"], "rb").read())

# make a prediction on the image
preds = model.predict(image)

# find the class label index with the largest corresponding
# probability
i = preds.argmax(axis=1)[0]
label = lb.classes_[i]
print(preds)
print(lb.classes_)
'''
(Pdb) preds
array([[5.4622066e-01, 4.5377851e-01, 7.7963534e-07]], dtype=float32)
'''

# draw the class label + probability on the output image
text = "{}: {:.2f}%".format(label, preds[0][i] * 100)
# (frame, text, location, font type, font size, font color, font boldness)
cv2.putText(output, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
            (128, 0, 0), 2)

# show the output image
cv2.imshow("Image", output)
cv2.waitKey(0)
