#!/usr/bin/env python3
# coding: utf-8
import cv2
import os
import numpy as np
# ArUcoのライブラリを導入
aruco = cv2.aruco

# 4x4のマーカー, IDは50までの辞書を使用
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
image_dir = "images"
result_dir = "results"



def recognizeArMarker(input_files):
    for i in range(len(input_files)):
        # 入力ファイル名
        # input_file_nm = "ar" + str(i) + ".png"
		# 出力ファイル名
        output_file_nm = "ar_detection" + str(i) + ".png"
		# 入力ファイルの読み込み
        input_path = os.path.join(image_dir, input_files[i])
        input_img = cv2.imread(input_path)
		# ArUcoマーカの検出
        corners, ids, rejectedCandidates = aruco.detectMarkers(input_img, dictionary, parameters=parameters)
        ids = np.ravel(ids)
        print(f"Detected marker IDs: {ids}")
        num_ids = [0, 8]
        for num_id in num_ids:
            if num_id in ids:
                index = np.where(ids == num_id)[0][0] #num_id が格納されているindexを抽出
                cornerUL = corners[index][0][0]
                cornerUR = corners[index][0][1]
                cornerBR = corners[index][0][2]
                cornerBL = corners[index][0][3]

                center = [ (cornerUL[0]+cornerBR[0])/2 , (cornerUL[1]+cornerBR[1])/2 ]
                
                print(f"Marker ID: {num_id}")
                print('左上 : {}'.format(cornerUL))
                print('右上 : {}'.format(cornerUR))
                print('右下 : {}'.format(cornerBR))
                print('左下 : {}'.format(cornerBL))
                print('中心 : {}'.format(center))
                print()

            cv2.drawMarker(input_img, (int(center[0]), int(center[1])), (255, 0, 255), thickness=5)
        # ArUcoマーカの検出結果の描画
        ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)
        cv2.drawMarker(input_img, (0, 0), (255, 0, 255), thickness=5)
        cv2.drawMarker(input_img, (1920, 1080), (255, 0, 255), thickness=5)

		# ArUcoマーカの検出結果をファイル出力
        output_path = os.path.join(result_dir, output_file_nm)
        cv2.imwrite(output_path, ar_image)

if __name__ == "__main__":
    """ cnt = 5
    input_files = [f"test_{i}.jpg" for i in range(cnt)] """
    input_files = ["9_qr.jpg"]
    recognizeArMarker(input_files)
