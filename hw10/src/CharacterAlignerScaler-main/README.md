# CharacterAlignerScaler

CharacterAlignerScaler 是一個用於對齊和縮放字符圖像的工具。它允許您根據指定的比例和最小尺寸來處理字符圖像，並將結果保存到指定的輸出文件夾。此外，本專案還包含一個用於顯示對齊和縮放操作前後的字符圖像的程式碼片段。

## 為什麼需要？

因為在稿紙上面寫的時候，我們是一個字一個字的寫，沒有左邊和上下的文字對照，我們寫的大小可能會忽大忽小，而如果不處理直接切成png，再轉成svg做成字體，出現的字可能會歪歪的，或是大小不一，或是「白邊太多」。所以這個repo就是來處理這些png，align就是把每一個char對齊中間；scale就是把白邊切掉，留下文字的部分，要留多少白邊，可以調scale的%數。

* 所以你現在需要一個，「經過切割完後的png檔案資料夾」，才能執行這個程式

但因為每一個中文字的邊框都差不多，所以抓到的方框會差不多，可是如果是非中文字，像是標點符號之類的，抓到的邊框就會很小，這樣程式運算上會有問題，所以目前的做法是，把所有非中文字的部分，跳過不做，以及再設一個最小邊界框尺寸，如果抓到的邊框小於這個尺寸，就跳過不處理。

## 切割的範例

原本會長這樣：
<img width="936" alt="image" src="https://user-images.githubusercontent.com/111958211/236994859-f0ee8ba7-8422-46df-a531-10b6cf5eeba3.png">

經過此程式碼處理後，變成這樣(字體大小設定一致)，v1：
<img width="917" alt="image" src="https://user-images.githubusercontent.com/111958211/236994963-c32d6eb4-af0c-4a49-8dc3-623ac7d96e83.png">

來源：助教的pdf稿紙

因為現在是每一個字都抓到它的邊框，並且統一放大到300x300的png，如果抓到的邊框小，字體會放大許多，也就會讓字跡變粗。所以目前的結果還是有很多需要改善的地方，所以如果大家有更好的想法或是程式設計，歡迎和我或是助教討論


## 功能

- 對齊字符圖像：根據字符的邊界框將字符放在新圖像的中心
- 縮放字符圖像：根據指定的縮放百分比來縮放字符(非中文字跳過，不處理)
- 顯示操作前後的字符圖像對比

## 安裝

1. clone這個專案：
```
git clone https://github.com/TaylorNTUT/CharacterAlignerScaler.git
```

2. 切換到專案目錄：
```
cd CharacterAlignerScaler
```

3. 創建並激活虛擬環境（可選）：
```
python -m venv venv
source venv/bin/activate 
```
* 在 Windows 上使用 venv\Scripts\activate

4. 安裝所需的依賴項：
```
pip install -r requirements.txt
```


## 使用方法

### align_and_scale_chr.py

* 把要處理的資料夾放到CharacterAlignerScaler這個資料夾下

執行以下命令來使用 CharacterAlignerScaler：
```
python align_and_scale_chr.py -f INPUT_FOLDER -o OUTPUT_FOLDER [-S] [-s SCALE_PERCENTAGE] [-m MIN_SIZE] [-A]
```
- `-f`, `--input-folder`: 包含 .png 文件的輸入文件夾
- `-o`, `--output-folder`: 處理後圖像的輸出文件夾(如果沒有會建一個)
- `-S`, `--scale`: 執行縮放操作
- `-s`, `--scale-percentage`: 縮放操作的縮放百分比（默認值：95）
- `-m`, `--min-size`: 最小邊界框尺寸百分比，也就是如果opencv抓到低於這個尺寸的邊框，不處理（默認值：50）
- `-A`, `--align`: 執行對齊操作


### compare.py (用來顯示操作前後的字符圖像對比)

使用下面的程式碼片段來顯示對齊和縮放操作前後的字符圖像對比：

注意：在運行顯示操作前後的字符圖像對比的程式碼片段之前，請確保已將 `before_folder` 和 `after_folder` 變量替換為實際的輸入和輸出文件夾名稱。

```python
before_folder = "./1_138"  # 請將 "./1_138" 替換換成實際的輸入文件夾名稱
after_folder = "1_138_after" # 請將 "1_138_after" 替換成實際的輸出文件夾名稱
display_images(before_folder, after_folder, 10) # 最後一個參數表示要展示的圖像對的數量
```


## 範例

要對 `1_138` 文件夾中的圖像進行對齊和縮放，並將結果保存到 `1_138_after` 文件夾，可以使用以下命令：
```
python align_and_scale_chr.py -f 1_138 -o 1_138_after -S -A
```

要對 `1_138` 文件夾中的圖像進行對齊和「縮放操作的縮放百分比：90」和「最小邊界框尺寸：60」，並將結果保存到 `1_138_after` 文件夾，可以使用以下命令：
```
python align_and_scale_chr.py -f 1_138 -o 1_138_after -S -A -s 90 -m 60
```

要對 `1_138` 和 `1_138_after` 裡面的圖像隨機抽取10個做比較，並輸出比較的圖：
```
python compare.py
```








