import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
img_counter = 1
video_counter = 1
while True:
    _, frame = cam.read()
    #cv2.imshow("streaming", frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # cv2.line(img, (320, 0), (320, 640), (0, 255, 0), 5)
    cv2.line(frame, (240, 0), (240, 640), (255, 255, 255), 2)
    cv2.line(frame, (400, 0), (400, 640), (255, 255, 255), 2)
    for (x, y, w, h) in faces:
        a = x + w / 2
        b = y + h / 2
        if a > 400:
            print("<====== Turn left")
        elif a < 240:
            print("Turn right =====>")
        
        cv2.rectangle(frame, (int(x + w / 2), int(y + h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255), 10)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(frame, (int(x + w / 2), int(y + h / 2)), (int(x + w / 2), int(y + h / 2)), (0, 0, 255), 10)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

    k = cv2.waitKey(1)
    print("streaming")
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
    cv2.imshow("streaming", frame)
cam.release()
cv2.destroyAllWindows()
