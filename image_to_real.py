#!/usr/bin/env python3
# coding: utf-8
import cv2
import os
import numpy as np
from estimator import convert_oracle_to_image_pos, convert_image_to_table_pos
# ArUcoのライブラリを導入
aruco = cv2.aruco

# 4x4のマーカー, IDは50までの辞書を使用
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
image_dir = "images"
result_dir = "results"

table_pos_dict = {
    0: [0, 0],
    1: [15, 0],
    2: [0, 15],
    3: [15, 15]
}

image_pos_dict = {
    0: [0, 0],
    1: [0, 0],
    2: [0, 0],
    3: [0, 0]
}

target_oracle_pos = [8, 6]
target_image_pos = [100, 100]

def recognizeArMarker(input_files):
    for idx, input_file in enumerate(input_files):
        # set output file name
        output_file_nm = f"result_{idx}.png"
	    # read input image
        input_path = os.path.join(image_dir, input_file)
        input_img = cv2.imread(input_path)
	    # detect AruCo marker
        corners, ids, rejectedCandidates = aruco.detectMarkers(input_img, dictionary, parameters=parameters)
        ids = np.ravel(ids)
        print(f"Detected marker IDs: {ids}")
        num_ids = [0, 1, 2, 3]
        for num_id in num_ids:
            if num_id in ids:
                index = np.where(ids == num_id)[0][0] #num_id が格納されているindexを抽出
                cornerUL = corners[index][0][0]
                cornerUR = corners[index][0][1]
                cornerBR = corners[index][0][2]
                cornerBL = corners[index][0][3]
                center = [ (cornerUL[0]+cornerBR[0])/2 , (cornerUL[1]+cornerBR[1])/2 ]

                image_pos_dict[num_id] = cornerUL
                print(f"Marker ID: {num_id}")
                print('左上 : {}'.format(cornerUL))
                # print('右上 : {}'.format(cornerUR))
                # print('右下 : {}'.format(cornerBR))
                # print('左下 : {}'.format(cornerBL))
                # print('中心 : {}'.format(center))
                print()
            cv2.drawMarker(input_img, (int(center[0]), int(center[1])), (255, 0, 255), thickness=5)
        # ArUcoマーカの検出結果の描画
        ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)

        # for testing, convert target_table_pos to target_image_pos
        target_image_pos = convert_oracle_to_image_pos(image_pos_dict, target_oracle_pos)
        cv2.drawMarker(ar_image, target_image_pos, (255, 255, 0), markerType=cv2.MARKER_TRIANGLE_UP, markerSize=50)

        # convert target_image_pos to target_table_pos and evaluate diff
        target_table_pos = convert_image_to_table_pos(image_pos_dict, table_pos_dict, target_image_pos)
        diff = np.linalg.norm(np.array(target_oracle_pos) - np.array(target_table_pos))
        print(f"Diff: {diff}")

	    # ArUcoマーカの検出結果をファイル出力
        output_path = os.path.join(result_dir, output_file_nm)
        cv2.imwrite(output_path, ar_image)

if __name__ == "__main__":
    input_files = ["cat_40.jpg", "cat_60.jpg", "cat_80.jpg"]
    recognizeArMarker(input_files)
