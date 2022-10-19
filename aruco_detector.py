#!/usr/bin/env python3
# coding: utf-8
import cv2
import os
# ArUcoのライブラリを導入
aruco = cv2.aruco

# 4x4のマーカー, IDは50までの辞書を使用
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters_create()
image_dir = "images"
result_dir = "results"

cnt = 4

def recognizeArMarker():
    for i in range(cnt + 1):
        # 入力ファイル名
        # input_file_nm = "ar" + str(i) + ".png"
        input_file_nm = f"test_{i}.jpg"
		# 出力ファイル名
        output_file_nm = "ar_detection" + str(i) + ".png"
		# 入力ファイルの読み込み
        input_path = os.path.join(image_dir, input_file_nm)
        input_img = cv2.imread(input_path)
		# ArUcoマーカの検出
        corners, ids, rejectedCandidates = aruco.detectMarkers(input_img, dictionary, parameters=parameters)
		# ArUcoマーカの検出結果の描画
        ar_image = aruco.drawDetectedMarkers(input_img, corners, ids)

		# ArUcoマーカの検出結果をファイル出力
        output_path = os.path.join(result_dir, output_file_nm)
        cv2.imwrite(output_path, ar_image)

if __name__ == "__main__":
    recognizeArMarker()
