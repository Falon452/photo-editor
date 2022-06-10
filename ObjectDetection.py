from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image
from imutils.object_detection import non_max_suppression


class ObjectDetection:
    def __init__(self, parent):
        self.parent = parent
        self.face_cascade = None
        self.smile_cascade = None
        self.cars_cascade = None

    def detect_face(self, img):
        img = np.array(img)
        if not self.face_cascade:
            self.face_cascade = cv2.CascadeClassifier()

        if not self.face_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_frontalface_alt.xml')):
            print('--(!)Error loading face cascade')
            exit(0)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.equalizeHist(img_gray)

        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5)

        print(f"Number of faces detected: {len(faces)}")

        for (x, y, w, h) in faces:
            center = (x + w // 2, y + h // 2)
            img = cv2.ellipse(img, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)

        res = Image.fromarray(img)
        return res

    def detect_smile(self, img):
        img = np.array(img)
        if not self.smile_cascade:
            self.smile_cascade = cv2.CascadeClassifier()
        if not self.face_cascade:
            self.face_cascade = cv2.CascadeClassifier()

        if not self.face_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_frontalface_alt.xml')):
            print('--(!)Error loading face cascade')
            exit(0)
        if not self.smile_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_smile.xml')):
            print('--(!)Error loading smile cascade')
            exit(0)

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.equalizeHist(img_gray)

        faces = self.face_cascade.detectMultiScale(img_gray, scaleFactor=1.05, minNeighbors=5)

        for (x, y, h, w) in faces:
            face = img[y: y + h, x: x + w, :]
            face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face_gray = cv2.equalizeHist(face_gray)

            smiles = self.smile_cascade.detectMultiScale(face_gray, scaleFactor=1.05, minNeighbors=11)

            for (x1, y1, w1, h1) in smiles:
                center = (x + x1 + w1 // 2, y + y1 + h1 // 2)
                img = cv2.ellipse(img, center, (w1 // 2, h1 // 2), 0, 0, 360, (249, 215, 18), 3)

        res = Image.fromarray(img)
        return res

    def detect_full_body(self, img):
        img = np.array(img)

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        (humans, _) = hog.detectMultiScale(img,
                                           winStride=(4, 4),
                                           padding=(8, 8),
                                           scale=1.03)

        humans = np.array([[x, y, x + w, y + h] for (x, y, w, h) in humans])
        humans = non_max_suppression(humans, probs=None, overlapThresh=0.45)
        print('Humans detected: ', len(humans))

        for (x, y, x1, y1) in humans:
            cv2.rectangle(img, (x, y),
                          (x1, y1),
                          (0, 0, 255), 2)

        res = Image.fromarray(img)
        return res

    def detect_cars(self, img):
        img = np.array(img)
        if not self.cars_cascade:
            self.cars_cascade = cv2.CascadeClassifier()

        if not self.cars_cascade.load(cv2.samples.findFile('haarcascades\haarcascade_cars.xml')):
            print('--(!)Error loading cars cascade')
            exit(0)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cars = self.cars_cascade.detectMultiScale(gray, 1.1, 1)

        cars = np.array([[x, y, x + w, y + h] for (x, y, w, h) in cars])
        cars = non_max_suppression(cars, probs=None, overlapThresh=0.45)

        for (x, y, x1, y1) in cars:
            cv2.rectangle(img, (x, y),
                          (x1, y1),
                          (0, 0, 255), 2)

        res = Image.fromarray(img)
        return res

    def detect_edges(self, img):
        img = np.array(img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
        corners = np.int0(corners)

        for i in corners:
            x, y = i.ravel()
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

        res = Image.fromarray(img)
        return res

    def pattern_match(self, img):
        NO_MATCHES = 5

        original = np.array(img)

        filepath = filedialog.askopenfilename(initialdir="/", title="Select a pattern",
                                              filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg"),
                                                         ("all files", "*.*")))

        pattern = cv2.imread(filepath)  # trainImage
        pattern = Image.fromarray(pattern)
        pattern = pattern.convert('RGB')
        pattern = np.array(pattern)

        gray_face = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        gray_pattern = cv2.cvtColor(pattern, cv2.COLOR_RGB2GRAY)

        orb = cv2.ORB_create()
        original_keypoints, original_descriptor = orb.detectAndCompute(gray_face, None)
        query_keypoints, query_descriptor = orb.detectAndCompute(gray_pattern, None)
        keypoints_without_size = np.copy(original)
        keypoints_with_size = np.copy(original)

        cv2.drawKeypoints(original, original_keypoints, keypoints_without_size, color=(0, 255, 0))
        cv2.drawKeypoints(original, original_keypoints, keypoints_with_size, flags=
        cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = brute_force.match(original_descriptor, query_descriptor)
        matches = sorted(matches, key=lambda x: x.distance)

        matches = matches[:NO_MATCHES]

        result = cv2.drawMatches(original, original_keypoints, gray_pattern, query_keypoints, matches,
                                 gray_pattern, flags=2)
        print("The number of matching keypoints between the original and the query image is {}\n".format(len(matches)))

        res = Image.fromarray(result)
        return res
