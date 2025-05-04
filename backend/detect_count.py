import torch
import cv2
from shapely.geometry import box

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
model.classes = [0, 60]
model.eval()

def detect_and_count(img_path: str, conf_thres: float = 0.3, output_path: str = None):
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = model(img_rgb)
    det = results.xyxy[0].cpu().numpy()

    tables = []
    people = []

    for x1, y1, x2, y2, conf, cls in det:
        if conf < conf_thres:
            continue
        cls = int(cls)
        color = (0, 255, 0) if cls == 0 else (255, 0, 0)
        label = 'Person' if cls == 0 else 'Table'
        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        cv2.putText(img, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if cls == 60:  # стол
            tables.append({'box': [float(x1), float(y1), float(x2), float(y2)], 'count': 0})
        elif cls == 0:  # человек
            people.append([float(x1), float(y1), float(x2), float(y2)])

    from shapely.geometry import box as shapely_box
    for pb in people:
        person_poly = shapely_box(pb[0], pb[1], pb[2], pb[3])
        for tbl in tables:
            tbl_poly = shapely_box(*tbl['box'])
            if tbl_poly.intersects(person_poly):
                tbl['count'] += 1
                break

    if output_path:
        cv2.imwrite(output_path, img)

    return {
        'tables': tables,
        'people_total': len(people),
        'img_url': output_path
    }