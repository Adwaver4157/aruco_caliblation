#!/usr/bin/env python3
# coding: utf-8
import cv2
import numpy as np
import os
# ArUcoのライブラリを導入
aruco = cv2.aruco

# 4x4のマーカ, IDは50までの辞書を使用
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
image_dir = "images"
pixel = 150
offset = 10
cnt = 9

def generateArMarker():
	# 白いブランク画像を生成
	img = np.zeros((pixel + offset, pixel + offset), dtype=np.uint8)
	img += 255

	x_offset = y_offset = int(offset) // 2
	# 9枚のマーカを作成する
	for i in range(cnt):
		# 150x150ピクセルで画像を作成
		ar_image = aruco.drawMarker(dictionary, i, pixel, 3)
		# ファイル名の指定
		filename = "ar" + str(i) + ".png"
		# ブランク画像の上にArUcoマーカを重ねる
		img[y_offset:y_offset + ar_image.shape[0], x_offset:x_offset + ar_image.shape[1]] = ar_image
		# グレースケールからRGBへ変換
		rgb_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
		
		# ArUcoマーカの画像を結合
		# 左端の時はそのまま水平方向用のbufferに代入
		if (i % 3 == 0):
			hconcat_img = rgb_img
		# 右端まで達するまで水平用bufferにconcat
		elif (i % 3 <= 2):
			hconcat_img = cv2.hconcat([hconcat_img, rgb_img])
			# 右端まで行きかつ１段目の時は鉛直方向用bufferに代入
			if (i % 3 == 2 and i // 3 == 0):
				vconcat_img = hconcat_img
			# 右端まで行きかつ２段目以降の時は鉛直方向にconcat
			elif (i % 3 == 2 and i // 3 > 0):
				vconcat_img = cv2.vconcat([vconcat_img, hconcat_img])

		# 1枚ごとのArUcoマーカを出力
		file_path = os.path.join(image_dir, filename)
		cv2.imwrite(file_path, rgb_img)

	# 結合したArUcoマーカを出力
	filename = "ar" + str(cnt) + ".png"
	file_path = os.path.join(image_dir, filename)
	cv2.imwrite(file_path, vconcat_img)
        
if __name__ == "__main__":
    generateArMarker()