from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
from skimage.util import img_as_ubyte
from skimage.transform import rescale, resize, downscale_local_mean
from skimage import data, color, img_as_float
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    defect_points_str = request.form.get('defect_points')
    normal_points_str = request.form.get('normal_points')

    if not defect_points_str or not normal_points_str:
        return "하자 부위와 정상 부위를 그려주세요.", 400

    defect_points = [tuple(map(int, p.split(','))) for p in defect_points_str.split(';')[:-1]]
    normal_points = [tuple(map(int, p.split(','))) for p in normal_points_str.split(';')[:-1]]

    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # 정상 부위와 하자 부위의 bounding rect 추출
    defect_rect = cv2.boundingRect(np.array(defect_points))
    normal_rect = cv2.boundingRect(np.array(normal_points))

    # 정상 부위의 패치 추출
    normal_patch = image[normal_rect[1]:normal_rect[1] + normal_rect[3], normal_rect[0]:normal_rect[0] + normal_rect[2]]

    # 정상 부위의 패치를 하자 부위의 크기로 리사이즈
    resized_normal_patch = cv2.resize(normal_patch, (defect_rect[2], defect_rect[3]))

    # 하자 부위에 정상 부위의 리사이즈된 패치 적용
    for i in range(defect_rect[3]):
        for j in range(defect_rect[2]):
            if cv2.pointPolygonTest(np.array(defect_points), (defect_rect[0] + j, defect_rect[1] + i), False) >= 0:
                image[defect_rect[1] + i, defect_rect[0] + j] = resized_normal_patch[i, j]

    _, buf = cv2.imencode('.png', image)
    response = BytesIO(buf.tobytes())
    return send_file(response, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

