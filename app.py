from flask import Flask, Response
import cv2

# ======================================
# GANTI dengan URL stream IP Webcam
# ======================================
URL_STREAM = "http://10.183.176.123:8080/video"  

app = Flask(__name__)

def generate_frames():
    cap = cv2.VideoCapture(URL_STREAM)

    while True:
        success, frame = cap.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/video")
def video():
    return Response(generate_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/")
def index():
    return """
    <h2>LIVE IP Webcam Camera</h2>
    <img src='/video' width='100%'>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
