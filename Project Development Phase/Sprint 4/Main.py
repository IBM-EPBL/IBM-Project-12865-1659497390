import cv2
import numpy as np
from keras.utils import load_img, img_to_array
from keras.models import load_model
from twilio.rest import Client
from playsound import playsound
from decouple import config

message_sent = False

model = load_model("./model.h5")

video = cv2.VideoCapture('fire.mp4')

name = ["No fire", "Fire Detected"]


def send_message():
    account_sid = config("AC608d828cb39c22aa9d46ba5652f1d05b")
    auth_token = config("d55ebbf16c1a66e0beed25ca9f5f53e8")

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="Forest Fire detected , Stay safe!!!",
        from_=config("+14793338520"),
        to=config("+91 9842425495")
    )
    print(message.sid)
    print("Fire Detected")
    print("SMS Sent!")

while True:
    success, frame = video.read()
    cv2.imwrite('Z:\\Fist\\image.jpg', frame)
    img = load_img('Z:\\Fist\\image.jpg', target_size=(128, 128))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict(x, verbose=0)
    p = int(pred[0][0])
    cv2.putText(frame, str(name[p]), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    if p == 1:
        if not message_sent:
            message_sent = True
            send_message()
        print("Fire Detected , stay safe!!!")
    else:
        print("No Fire Detected")

    cv2.imshow("Image", frame)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

video.release()
cv2.destroyAllWindows()
