import cv2
import numpy as np
import shutil
import os
import json
from tqdm import tqdm
import argparse


def read_json(file):
    with open(file) as f:
        p = json.load(f)
        v = [''] * 13759

        skip_ranges = [(0, 664), (13725, 13759)]

        for i in range(13759):
            if any(start <= i <= end for start, end in skip_ranges):
                if (128 <= i < 256) or (0 <= i < 32):
                    v[i] = '123'
                else:
                    v[i] = 'U+' + p['CP950'][i]['UNICODE'][2:6]
        return v

v = read_json('./CP950.json')


def align_and_scale_character(image_path, output_path, counters, scale_percentage=95, min_size=50):
    image_name = os.path.basename(image_path)
    image_name = image_name.split(".")

    if image_name[0] in v:
        counters["no_process"] += 1
        shutil.copyfile(image_path, output_path)
        return counters
    else:
        counters["process"] += 1

    # 如果沒有指定任何操作，則返回特殊值
    if scale_percentage is None and min_size is None:
        return "no_operation"

    # 讀取圖像
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 二值化圖像
    _, threshold = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

    # 計算水平和垂直方向的投影
    horizontal_projection = np.sum(threshold, axis=0)
    vertical_projection = np.sum(threshold, axis=1)

    # 尋找水平方向的最大方框
    result_left = np.where(horizontal_projection < 255 * img.shape[0])[0]
    if result_left.size > 0:
        left = result_left[0]
    else:
        left = 0

    result_right = np.where(horizontal_projection < 255 * img.shape[0])[0]
    if result_right.size > 0:
        right = result_right[-1]
    else:
        right = img.shape[1] - 1

    # 尋找垂直方向的最大方框
    result_top = np.where(vertical_projection < 255 * img.shape[1])[0]
    if result_top.size > 0:
        top = result_top[0]
    else:
        top = 0

    result_bottom = np.where(vertical_projection < 255 * img.shape[1])[0]
    if result_bottom.size > 0:
        bottom = result_bottom[-1]
    else:
        bottom = img.shape[0] - 1

    # 獲取最大方框的尺寸
    w = right - left + 1
    h = bottom - top + 1

    # 檢查方框是否小於指定的定值
    if w < min_size and h < min_size:
        print(f"The bounding box size (w: {w}, h: {h}) is smaller than the minimum size: {min_size}. Skipping.")
        shutil.copy(image_path, output_path)
        return

    # 根據最大方框中的字符創建一個新的白色圖像
    aligned_img = np.ones(img.shape, dtype=np.uint8) * 255


    if scale_percentage is not None:
        # 計算縮放後的尺寸
        target_w = int(img.shape[1] * (scale_percentage / 100))
        target_h = int(img.shape[0] * (scale_percentage / 100))

        # 計算縮放因子
        scale_w = target_w / w
        scale_h = target_h / h
        scale = min(scale_w, scale_h)

        # 縮放字符
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)

        # 使用 cv2.INTER_CUBIC 插值方法進行縮放
        scaled_img = cv2.resize(img[top:bottom+1, left:right+1], (scaled_w, scaled_h), interpolation=cv2.INTER_CUBIC)
    else:
        # 如果不進行縮放操作，則直接使用原始圖像
        scaled_w = w
        scaled_h = h
        scaled_img = img[top:bottom+1, left:right+1]


    # 將字符放置在新圖像的中心
    center_x = (img.shape[1] - scaled_w) // 2
    center_y = (img.shape[0] - scaled_h) // 2
    aligned_img[center_y:center_y+scaled_h, center_x:center_x+scaled_w] = scaled_img

    # 保存對齊並縮放後的圖像
    cv2.imwrite(output_path, aligned_img)

    return counters


def main(args):
    counters = {"process": 0, "no_process": 0}
    no_op_msg_printed = False

    input_folder = args.input_folder
    output_folder = args.output_folder
    scale_percentage = args.scale_percentage if args.scale else None
    min_size = args.min_size if args.align else None

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder)

    print(f"The output folder '{output_folder}' has been created.")

    for file_name in tqdm(os.listdir(input_folder)):
        if file_name.endswith('.png'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)
            result = align_and_scale_character(input_path, output_path, counters, scale_percentage, min_size)

            if result == "no_operation" and not no_op_msg_printed:
                print(f"Did not perform any operation, directly copied the data to the folder {os.path.dirname(output_path)}")
                no_op_msg_printed = True
            elif result != "no_operation":
                counters = result

    print(f"  A total of {counters['process']} files were processed. ")
    print(f"  A total of {counters['no_process']} files were not processed. ")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Align and scale character images.")
    parser.add_argument("-f", "--input-folder", type=str, required=True, help="Input folder with .png files.")
    parser.add_argument("-o", "--output-folder", type=str, required=True, help="Output folder for processed images.")
    parser.add_argument("-S", "--scale", action="store_true", help="Perform scale operation.")
    parser.add_argument("-s", "--scale-percentage", type=int, default=95, help="Scale percentage for scale operation (default: 95).")
    parser.add_argument("-m", "--min-size", type=int, default=50, help="Minimum bounding box size (default: 50).")
    parser.add_argument("-A", "--align", action="store_true", help="Perform align operation.")
    args = parser.parse_args()

    main(args)