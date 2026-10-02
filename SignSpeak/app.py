from pyngrok import ngrok

import streamlit as st
import cv2
import mediapipe as mp

st.set_page_config(page_title="SignSpeak")
st.title("SignSpeak - Voice for the Silent")
st.success("Hand Detection Ready! 0.10.14")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

run = st.checkbox('Start Camera')
FRAME = st.image([])
text_area = st.empty()

if run:
    cap = cv2.VideoCapture(0)
    while run:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)
        msg = "No Hand"
        if result.multi_hand_landmarks:
            for lm in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, lm, mp_hands.HAND_CONNECTIONS)
            msg = "Hello - Hand Detected!"
            cv2.putText(frame, msg, (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        FRAME.image(frame, channels="BGR")
        text_area.markdown(f"### Detected: {msg}")
    cap.release()
else:
    st.info("Camera start chey mawa")
    public_url = ngrok.connect(8501)
print(f"Public URL: {public_url}")