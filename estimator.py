import torch, detectoron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, cv2, random

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

def convert_oracle_to_image_pos(image_pos_dict, target_oracle_pos=[8, 6], table_size=[15, 15]):
    cornerUL = image_pos_dict[0]
    cornerDR = image_pos_dict[3]
    diff = cornerDR - cornerUL
    target_image_pos = target_oracle_pos * (diff / table_size) + cornerUL
    target_pos_int = [int(x) for x in target_image_pos]
    print(diff)
    print(target_pos_int)
    # target_image_pos = [100, 100]
    return target_pos_int

def detect_image_pos(image):
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    predictor = DefaultPredictor(cfg)
    outputs = predictor(image)
    v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
    out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
    cv2.imwrite('results/test.jpg', out.get_image()[:, :, ::-1])
    # cv2_imshow(out.get_image()[:, :, ::-1])
    target_image_pos = [100, 100]
    target_pos_int = [int(x) for x in target_image_pos]
    return target_pos_int

def convert_image_to_table_pos(image_pos_dict, table_pos_dict, target_image_pos, table_size=[15, 15]):
    cornerUL = image_pos_dict[0]
    cornerDR = image_pos_dict[3]
    diff = cornerDR - cornerUL
    target_table_pos = target_image_pos * (table_size / diff)
    # target_table_pos = [8, 6]
    return target_table_pos