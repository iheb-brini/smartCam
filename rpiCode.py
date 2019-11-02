#imports
import cv2
import RPi.GPIO as GPIO
import threading
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 50)
pwm.start(7)
GPIO.setwarnings(False)

oldangle=90

def turnleft(oldangle) :
    angle=oldangle-15
    duty = angle / 18. + 2
    pwm.ChangeDutyCycle(duty)
    return angle
def turnright(oldangle) :
    angle=oldangle+15
    duty = angle / 18. + 2
    pwm.ChangeDutyCycle(duty)
    return angle

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
img_counter = 1
video_counter = 1

while True:
    _, frame = cam.read()
    a = frame.shape[0]
    height,width = frame.shape[0],frame.shape[1]
    #cv2.imshow("streaming", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # cv2.line(img, (320, 0), (320, 640), (0, 255, 0), 5)
    cv2.line(frame, (width//3, 0), (width//3, height), (255, 255, 255), 2)
    cv2.line(frame, (2*width//3, 0), (2*width//3, height), (255, 255, 255), 2)

    cv2.line(frame, (width//2, 0), (width//2, height), (202, 25, 155), 2)    

    if len(faces) : 
        (x, y, w, h) = faces[0]
        a = x + w / 2
        b = y + h / 2
        if a > 2*width//3 and oldangle>30:
            tl=threading.Thread(target=turnleft,args=(oldangle,))
            tl.start()
            tl.join()
            oldangle=turnleft(oldangle)
            print("<====== Turn left")
        elif a < width//3:
            tr=threading.Thread(target=turnright,args=(oldangle,))
            tr.start()
            tr.join()
            print("Turn right =====>")

        cv2.rectangle(frame, (int(x + w / 2), int(y + h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255), 10)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC pressed
        print("closing")
        break

    elif k % 256 == 32:  # Space pressed
        print("capture")
        cv2.imwrite('opencv' + str(img_counter) + '.png', frame)
        img_counter += 1

    elif k % 256 == ord('r'):
        out = cv2.VideoWriter('output' + str(video_counter) + '.avi', fourcc, 20.0, (640, 480))
        while True:
            print("recording")
            cv2.destroyWindow('streaming')
            _, frame = cam.read()
            out.write(frame)
            cv2.imshow('recording', frame)
            k = cv2.waitKey(1)
            if k % 256 == ord('q'):
                print("closing")
                video_counter += 1
                out.release()
                cv2.destroyWindow('recording')

                break
                k = cv2.waitKey(1)
    if k % 256 == ord('q'):
        print("closing")
        break
    cv2.imshow("streaming", frame)
cam.release()
cv2.destroyAllWindows()
