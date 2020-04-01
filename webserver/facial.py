from PIL import Image
import face_recognition
import os, csv
import numpy as np
from numpy import savetxt

# Load the jpg file into a numpy array
i = 1
directory = './public/images/'
known_face_encodings = []
known_face_names = []
for subdir, dirs, files in os.walk(directory):
    for file in files:
        print((os.path.join(subdir, file)))
        image = face_recognition.load_image_file(os.path.join(subdir, file))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        #known_face_names.append(os.path.basename(subdir))
#
#savetxt('data.csv', known_face_encodings, delimiter=',')
#with open ('knownFaces.csv', 'wb') as f:
   # csv.writer(f).writerows(known_face_names)
#savetxt('data2.csv', known_face_names, delimiter=',')
with open('knownFaces.csv', 'a+', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([os.path.basename(subdir)])
# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py