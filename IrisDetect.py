import cv2
import numpy as np



eye = cv2.CascadeClassifier('haarcascade_eye.xml')
face = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

Kernal = np.ones((3, 3), np.uint8)      

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 400)      
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)




while 1:
    ret, frame = cap.read()                    
    frame = cv2.flip(frame, +1)                     
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      
    detect_face = face.detectMultiScale(gray, 1.2, 1)   
    detect_eye = eye.detectMultiScale(gray, 1.2, 1)

    for(face_x, face_y, face_z, face_h) in detect_face:
        img2 = gray[face_y:face_y+face_h, face_x:face_x+face_z]
        detect_eye = eye.detectMultiScale(img2, 1.2, 1)
        for (eye_x, eye_y, eye_z, eye_h) in detect_eye:
           
            eye1 = gray[face_y+eye_y:face_y+eye_y+eye_h, face_x+eye_x:face_x+eye_x+eye_z]

            ret, binary = cv2.threshold(eye1, 60, 255, cv2.THRESH_BINARY_INV)
            

            width, height = binary.shape
            binary = binary[int(0.4 * height):height, :]   

            opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, Kernal)  
            dilate = cv2.morphologyEx(opening, cv2.MORPH_DILATE, Kernal)  

            contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE,  
                                                   cv2.CHAIN_APPROX_NONE)
            if len(contours) != 0:
                cnt = contours[0]
                M1 = cv2.moments(cnt)

                Cx1 = int(M1['m10'] / M1['m00'])        
                Cy1 = int(M1['m01'] / M1['m00'])
                croppedImagePixelLength = int(0.4*height)      
                center1 = (int(Cx1+face_x+eye_x), int(Cy1+face_y + eye_y + croppedImagePixelLength))    
                cv2.circle(frame, center1, 2, (0, 255, 0), 2)
    if not ret:                    
        break
    if cv2.waitKey(1) == ord('s'): 
        break
    cv2.imshow('Frame Image', frame)        

cap.release()
cv2.destroyAllWindows()