import numpy as np
import cv2
import re
import sqlite3
import os
import math
label = [
    "1a", "1b", "1c", "1d", "21a", "21b", "21c", "21d", "41a", "41b", "41c", "41d", "61a", "61b", "61c", "61d",
    "2a", "2b", "2c", "2d", "22a", "22b", "22c", "22d", "42a", "42b", "42c", "42d", "62a", "62b", "62c", "62d",
    "3a", "3b", "3c", "3d", "23a", "23b", "23c", "23d", "43a", "43b", "43c", "43d", "63a", "63b", "63c", "63d",
    "4a", "4b", "4c", "4d", "24a", "24b", "24c", "24d", "44a", "44b", "44c", "44d", "64a", "64b", "64c", "64d",
    "5a", "5b", "5c", "5d", "25a", "25b", "25c", "25d", "45a", "45b", "45c", "45d", "65a", "65b", "65c", "65d",
    "6a", "6b", "6c", "6d", "26a", "26b", "26c", "26d", "46a", "46b", "46c", "46d", "66a", "66b", "66c", "66d",
    "7a", "7b", "7c", "7d", "27a", "27b", "27c", "27d", "47a", "47b", "47c", "47d", "67a", "67b", "67c", "67d",
    "8a", "8b", "8c", "8d", "28a", "28b", "28c", "28d", "48a", "48b", "48c", "48d", "68a", "68b", "68c", "68d",
    "9a", "9b", "9c", "9d", "29a", "29b", "29c", "29d", "49a", "49b", "49c", "49d", "69a", "69b", "69c", "69d",
    "10a", "10b", "10c", "10d", "30a", "30b", "30c", "30d", "50a", "50b", "50c", "50d", "70a", "70b", "70c", "70d",
    "11a", "11b", "11c", "11d", "31a", "31b", "31c", "31d", "51a", "51b", "51c", "51d", "71a", "71b", "71c", "71d",
    "12a", "12b", "12c", "12d", "32a", "32b", "32c", "32d", "52a", "52b", "52c", "52d", "72a", "72b", "72c", "72d",
    "13a", "13b", "13c", "13d", "33a", "33b", "33c", "33d", "53a", "53b", "53c", "53d", "73a", "73b", "73c", "73d",
    "14a", "14b", "14c", "14d", "34a", "34b", "34c", "34d", "54a", "54b", "54c", "54d", "74a", "74b", "74c", "74d",
    "15a", "15b", "15c", "15d", "35a", "35b", "35c", "35d", "55a", "55b", "55c", "55d", "75a", "75b", "75c", "75d",
    "16a", "16b", "16c", "16d", "36a", "36b", "36c", "36d", "56a", "56b", "56c", "56d", "66a", "66b", "66c", "66d",
    "17a", "17b", "17c", "17d", "37a", "37b", "37c", "37d", "57a", "57b", "57c", "57d", "77a", "77b", "77c", "77d",
    "18a", "18b", "18c", "18d", "38a", "38b", "38c", "38d", "58a", "58b", "58c", "58d", "78a", "78b", "78c", "78d",
    "19a", "19b", "19c", "19d", "39a", "39b", "39c", "39d", "59a", "59b", "59c", "59d", "79a", "79b", "79c", "79d",
    "20a", "20b", "20c", "20d", "40a", "40b", "40c", "40d", "60a", "60b", "60c", "60d", "80a", "80b", "80c", "80d",
]
calibrated = {}
calibPoint = (99, 240)
answers = []
student_ans = []
response = []
def sorted_nicely(l):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)
def readAnswerKey(filename):
    global student_ans

    f = open(filename, "r")
    for x in f:
        answers.append(x.rstrip() )
    answers.sort()
    sorted = sorted_nicely(student_ans)
    score = set(answers) & set(student_ans)

    db = sqlite3.connect('math.db')
    cursor = db.cursor()
    query = "INSERT INTO answers(student_id, test_id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29, q30, q31, q32, q33, q34, q35, q36, q37, q38, q39, q40, score) VALUES (9999, 9999, "
    for x in sorted:
        query += "'" + x + "', "
    query += str(len(score) ) + ");"
    cursor.execute(query)
    db.commit()
    db.close()
    
def loadAnswerSheet(filename):
    global student_ans
    global response

    fullPath = os.path.join('tmp', filename)
    raw = cv2.imread(fullPath)
    #image = cv2.GaussianBlur(raw, (5, 5), 1)
    image = raw
    grayScale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(grayScale, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    sigma = 0.33
    v = np.median(image)
    low = int(max(0, (1.0 - sigma) * v))
    high = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(grayScale, low, high)
    (cnts, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    shift = (0, 0, 0, 0)
    for c in cnts[::-1]:
        if calibration(c) != (0, 0, 0, 0):
            if abs(calibration(c)[0]-99)<40 and abs(calibration(c)[1]-240)<30:
                shift = calibration(c)
                #print shift
                break
    student_ans = []
    histogram = [0] * 20
    for k, v in calibrated.items():
        zeros = np.zeros((v[3], v[2]), np.uint8)
        cx = v[0] - calibPoint[0] + shift[0] 
        cy = v[1] - calibPoint[1] + shift[1]
        cv2.rectangle(image, (cx, cy), (cx+v[2], cy+v[3]), (0, 255, 0), 2 );
        im = thresh[cy:cy+v[3], cx:cx+v[2] ]
        mask = cv2.bitwise_and(im, im, zeros)
        blanks = float(v[3]*v[2])
        total = float(cv2.countNonZero(mask)/blanks)
	histogram[int(math.floor(total*20) )] += 1

    #histogram to find proper threshold for selecting answer
    rsum = 0;
    for i in range( len(histogram) - 1, -1, -1):
        rsum += histogram[i]
        if rsum == 40:
            darkthreshold = i-1
            break
    darkthreshold = float(darkthreshold/20.)
        
    for k, v in calibrated.items():
        zeros = np.zeros((v[3], v[2]), np.uint8)
        cx = v[0] - calibPoint[0] + shift[0] 
        cy = v[1] - calibPoint[1] + shift[1]
        cv2.rectangle(image, (cx, cy), (cx+v[2], cy+v[3]), (0, 255, 0), 2 );
        im = thresh[cy:cy+v[3], cx:cx+v[2] ]
        mask = cv2.bitwise_and(im, im, zeros)
        blanks = float(v[3]*v[2])
        total = float(cv2.countNonZero(mask)/blanks)
        if total >= darkthreshold:
	    questionnumber = int(re.sub("[^0-9]", "", k) )
            if questionnumber > 40:
                continue
            student_ans.append(k)
            cv2.putText(raw, str(k), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)
    student_ans = sorted_nicely(student_ans)
    if len(student_ans) != 40:
        response.append(str(len(student_ans) ) + " answered in " + filename)
        response.append(student_ans)
    print "<pre>"
    print darkthreshold, histogram, response
    print "<pre/>"
        
    resultPath = "result.png"
    cv2.imwrite(resultPath, raw)
def calibration(c):
    coord = (0, 0, 0, 0)
    area = cv2.contourArea(c, True)
    perimeter = cv2.arcLength(c, True)
    vertices = cv2.approxPolyDP(c, 0.01 * perimeter, True)
    x,y,w,h = cv2.boundingRect(c)
    if len(vertices) > 4 and area<0 and abs(h-18)<2 and (abs(w-25)<2 or abs(w-32)<2 or abs(w-30)<2) and (abs(w/float(h)-1.38)<0.2 or abs(w/float(h)-1.75)<0.2):
        coord = (x, y, w, h)
    return coord

def imagepro(filename):
    raw = cv2.imread("Scan_20190513_1.png") #empty answer sheet
    
    image = raw
    grayScale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sigma = 0.33
    v = np.median(image)
    low = int(max(0, (1.0 - sigma) * v))
    high = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(grayScale, low, high)
    (cnts, _) = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    boxes = []
    for c in cnts:
        coord = calibration(c)
        cv2.rectangle(image, (coord[0], coord[1]), (coord[0]+coord[2], coord[1]+coord[3]), (0, 255, 0), 2 );
        cv2.putText(image, str(coord[0]) + "," + str(coord[1]), (coord[0], coord[1]), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 2)
        if coord == (0, 0, 0, 0):
            continue
        boxes.append(coord)
    #boxes.sort(key=lambda b: b[1], reverse = True)
    
    l = 0
    for x, y, w, h in boxes[::-1]:
        if y>1300: #answers section
            calibrated[label[l] ] = (x, y, w, h)
            cv2.putText(image, label[l], (x, y), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 2)
            l+=1
    
    loadAnswerSheet(filename)
    readAnswerKey("answer.key")
    return response #array
