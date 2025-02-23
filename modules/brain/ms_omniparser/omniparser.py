import base64
import io
from typing import Dict
import time

import torch
from ultralytics import YOLO
from PIL import Image

from config import ICONDETECT_WEIGHTS_PATH, FLORENCE_WEIGHT_PATH, BOX_TRESHOLD
from modules.brain.ms_omniparser.utils import (
    get_som_labeled_img,
    check_ocr_box,
    get_caption_model_processor,
    get_yolo_model,
)
from tools.get_screenshot import get_screenshot

SOM_MODEL = None
CAPTION_MODEL_PROCESSOR = None


def initialize_models():
    """Function to initialize models if not already loaded."""
    device = "cuda"
    global SOM_MODEL, CAPTION_MODEL_PROCESSOR

    if SOM_MODEL is None:
        SOM_MODEL = get_yolo_model(model_path=ICONDETECT_WEIGHTS_PATH)
        SOM_MODEL.to(device)

    if CAPTION_MODEL_PROCESSOR is None:
        CAPTION_MODEL_PROCESSOR = get_caption_model_processor(
            model_name="florence2",
            model_name_or_path=FLORENCE_WEIGHT_PATH,
            device=device,
        )


initialize_models()


def get_screenshot_with_bounding_box(screenshot_path: str):

    start = time.time()
    image = Image.open(screenshot_path)
    box_overlay_ratio = image.size[0] / 3200
    draw_bbox_config = {
        "text_scale": 0.8 * box_overlay_ratio,
        "text_thickness": max(int(2 * box_overlay_ratio), 1),
        "text_padding": max(int(3 * box_overlay_ratio), 1),
        "thickness": max(int(3 * box_overlay_ratio), 1),
    }

    ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
        screenshot_path,
        display_img=False,
        output_bb_format="xyxy",
        goal_filtering=None,
        easyocr_args={"paragraph": False, "text_threshold": 0.9},
        use_paddleocr=True,
    )
    text, ocr_bbox = ocr_bbox_rslt

    dino_labled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
        screenshot_path,
        SOM_MODEL,
        BOX_TRESHOLD=BOX_TRESHOLD,
        output_coord_in_ratio=False,
        ocr_bbox=ocr_bbox,
        draw_bbox_config=draw_bbox_config,
        caption_model_processor=CAPTION_MODEL_PROCESSOR,
        ocr_text=text,
        use_local_semantics=True,
        iou_threshold=0.1,
        imgsz=640,
    )

    image = Image.open(io.BytesIO(base64.b64decode(dino_labled_img)))

    return_list = [
        {
            "id": i,
            "shape": {
                "x": coord[0],
                "y": coord[1],
                "width": coord[2],
                "height": coord[3],
            },
            "text": parsed_content_list[i].split(": ")[1],
            "type": "text",
        }
        for i, (k, coord) in enumerate(label_coordinates.items())
        if i < len(parsed_content_list)
    ]
    return_list.extend(
        [
            {
                "id": i,
                "shape": {
                    "x": coord[0],
                    "y": coord[1],
                    "width": coord[2],
                    "height": coord[3],
                },
                "text": "None",
                "type": "icon",
            }
            for i, (k, coord) in enumerate(label_coordinates.items())
            if i >= len(parsed_content_list)
        ]
    )

    simplified_return_list = [{obj["id"]: obj["text"]} for obj in return_list]

    file_path = screenshot_path.replace(".png", "_processed.png")
    image.save(file_path)

    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    file_path_base_64 = f"data:image/jpeg;base64,{image_base64}"

    print(f"Time taken by omniparser = {time.time() - start}")
    return file_path_base_64, return_list, simplified_return_list, screenshot_path
