# Youtube-Data-Analysis
此專案利用 YouTube API 自動化收集 YouTube 頻道的影片數據，包括訂閱數、總觀看次數、影片數量、影片詳細資訊及封面圖片，並將結果存入 CSV 檔案，方便後續進行分析。



## 前置準備
取得 YouTube API 金鑰

前往 Google Cloud Console。

建立新專案（或選擇現有專案）。

啟用 YouTube Data API v3 服務。

在 憑證 頁面中建立 API 金鑰，並複製該金鑰。

將此金鑰填入程式碼中的 api_key 變數。

## 功能說明
頻道資料查詢：根據頻道名稱查詢基本資訊（如訂閱數、總觀看次數、影片數量）。
影片 ID 提取：自動獲取指定頻道的所有影片 ID。
封面圖片下載：下載所有影片封面圖片，並以影片標題命名儲存。
影片數據提取：收集影片的發布日期、點閱率、喜歡數量等資訊，並匯出至 CSV 文件。

## 安裝與使用
1. 克隆專案
```bash
git clone https://github.com/hank-chu/Youtube-Data-Analysis.git
cd Youtube-Data-Analysis
```

2. 安裝相關套件
```bash
pip install -r requirements.txt
```

### 使用方法
設定 API 金鑰：
將 main.py 中的 api_key 替換為你的 YouTube API 金鑰
```bash
api_key = 'YOUR_API_KEY_HERE'
```

設定要分析的頻道名稱：
```bash
channel_name  = '你想分析的頻道名稱'
```

執行程式
```bash
python main.py
```
## 輸出結果
程式執行後會產生：
thumbnails/：儲存所有影片縮圖的資料夾
video_details/video_details.csv：包含以下影片資訊的 CSV 檔案
- 影片標題
- 影片 ID
- 發布日期
- 觀看次數
- 喜歡數
- 不喜歡數



