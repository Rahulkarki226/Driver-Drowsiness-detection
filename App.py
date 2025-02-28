import cv2
import os
from tensorflow.keras.models import load_model
import numpy as np
import streamlit as st

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")


def drowsiness_detection(model_path, alarm_sound='alarm.wav'):
    model = load_model("model.h5")

    lbl = ['Close', 'Open']

    path = os.getcwd()
    cap = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    score = 0

    while (True):
        ret, frame = cap.read()
        height, width = frame.shape[:2]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, minNeighbors=3, scaleFactor=1.1, minSize=(25, 25))
        eyes = eye_cascade.detectMultiScale(gray, minNeighbors=1, scaleFactor=1.1)

        cv2.rectangle(frame, (0, height - 50), (200, height), (0, 0, 0), thickness=cv2.FILLED)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)

        for (x, y, w, h) in eyes:

            eye = frame[y:y + h, x:x + w]
            # eye = cv2.cvtColor(eye,cv2.COLOR_BGR2GRAY)
            eye = cv2.resize(eye, (80, 80))
            eye = eye / 255
            eye = eye.reshape(80, 80, 3)
            eye = np.expand_dims(eye, axis=0)
            prediction = model.predict(eye)
            # print(prediction)
            # Condition for Close
            if prediction[0][0] > 0.30:
                cv2.putText(frame, "Closed", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                score = score + 1
                # print("Close Eyes")
                if (score > 20):
                    try:
                        sound.play()
                    except:  # isplaying = False
                        pass

            # Condition for Open
            elif prediction[0][1] > 0.70:
                score = score - 1
                if (score < 0):
                    score = 0
                cv2.putText(frame, "Open", (10, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
                # print("Open Eyes")
                cv2.putText(frame, 'Score:' + str(score), (100, height - 20), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


# Streamlit app
def main():
    st.title("Emotion Recognition App")

    # Click the button to start the webcam
    if st.button("Start Webcam"):
        drowsiness_detection(model_path=os.path.join('models', 'model.h5'))


# Run the Streamlit app
if __name__ == '__main__':
    main()