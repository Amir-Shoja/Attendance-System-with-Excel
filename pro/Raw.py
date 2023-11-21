import cv2 as cv
import cvzone
import os
import csv
import pickle
import face_recognition as fr
import numpy as np
from datetime import datetime
from openpyxl import Workbook


cap = cv.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# imgBackground = cv.imread("Resources/back/2.jpg")
imgBackground = cv.imread("Resources/background.png")

folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv.imread(os.path.join(folderModePath, path)))


print("LOADING ENCODE FILE START ...")
file = open("EncodeFile.p", "rb")
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, personIds = encodeListKnownWithIds
# print(personIds)
print("ENCODE FILE LOADED")

isNameWrittenDic = {}

while True:
    success, img = cap.read()

    imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceCurFrame = fr.face_locations(imgS)
    encodeCurFrame = fr.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[0]

    for encoFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = fr.compare_faces(encodeListKnown, encoFace)
        faceDis = fr.face_distance(encodeListKnown, encoFace)

        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            personID = personIds[matchIndex]
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            bbox = 55+x1, 162+y1, x2-x1, y2-y1
            imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
            imgBackground[44:44+633, 808:808+414] = imgModeList[1]
            cv.putText(imgBackground, personID,
                       (bbox[0]+10, bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (17, 0, 153), 2)
            if personID not in isNameWrittenDic or not isNameWrittenDic[personID]:
                name = personID
                print(personIds[matchIndex])
                isNameWrittenDic[personID] = True

        else:
            imgBackground[44:44+633, 808:808+414] = imgModeList[3]

    if success:
        height, width, _ = img.shape
        if height > 0 and width > 0:
            cv.imshow("Face Attendance", imgBackground)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Invalid image size.")
            break
    else:
        print("Failed to capture frame.")
        break
cv.destroyAllWindows()
