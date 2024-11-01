from googleapiclient.discovery import build
import sys
import os
import requests
import pandas as pd

# 設定輸出為 UTF-8 編碼，避免中文出現亂碼
sys.stdout.reconfigure(encoding='utf-8')

# 搜索頻道ID
def check_channel_id(channel_name):

    # 根據頻道名稱查詢頻道 ID。
    # 參數：
    #     channel_name (str): 要查詢的頻道名稱
    # 返回值：
    #     channel_id (str): 該頻道的頻道 ID

    request = youtube.search().list(
        part="snippet",
        q=channel_name,
        type="channel",
        maxResults=1
    )
    response = request.execute()

    print("頻道名稱與頻道ID如下")
    for item in response['items']:
        print("Channel Title:", item['snippet']['title'])
        print("Channel ID:", item['id']['channelId'])

    channel_id = response['items'][0]['id']['channelId']
    return channel_id


def check_channel_statistics(channel_id):

    # 根據頻道 ID 查詢頻道的統計資料，包括訂閱數、總觀看次數和影片數量。
    # 參數：
    #     channel_id (str): 要查詢的頻道 ID

    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    print("頻道詳細資訊如下")
    for item in response['items']:
        print("Channel Title:", item['snippet']['title'])
        print("Subscribers:", item['statistics']['subscriberCount'])
        print("Total Views:", item['statistics']['viewCount'])
        print("Video Count:", item['statistics']['videoCount'])
        print("Description:", item['snippet']['description'])
        print("---------------")


def get_all_video_ids(channel_id):

    # 取得指定頻道的所有影片 ID。
    # 參數：
    #     channel_id (str): 頻道 ID
    # 返回值：
    #     video_ids (list): 包含所有影片 ID 的列表

    video_ids = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='id',
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type='video'
        )
        response = request.execute()

        # 將每個影片的 ID 保存到列表
        for item in response['items']:
            video_ids.append(item['id']['videoId'])

        # 檢查是否還有下一頁
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids


def download_thumbnail(video_id, title, output_folder):

    # 根據影片 ID 下載影片的封面圖片。
    # 參數：
    #     video_id (str): 影片 ID
    #     title (str): 影片標題
    #     output_folder (str): 圖片存放的資料夾

    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()

    # 取得封面圖片 URL
    thumbnail_url = response['items'][0]['snippet']['thumbnails']['high']['url']
    # 將標題進行過濾，去除特殊字符，以便成為檔案名稱
    sanitized_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c == ' ']).rstrip()

    # 設定圖片檔案名稱和路徑
    file_name = f"{sanitized_title}.jpg"
    file_path = os.path.join(output_folder, file_name)

    # 下載圖片
    img_data = requests.get(thumbnail_url).content
    with open(file_path, 'wb') as handler:
        handler.write(img_data)

    print(f"下載完成: {file_name}")

# 下載指定頻道的所有影片封面圖片,儲存至thumbnails資料夾。
def download_all_thumbnails(channel_id):

    output_folder = 'thumbnails'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 取得所有影片 ID
    video_ids = get_all_video_ids(channel_id)

    for video_id in video_ids:
        # 取得影片標題並下載封面圖片
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()

        title = response['items'][0]['snippet']['title']
        
        download_thumbnail(video_id, title, output_folder)

# 取得影片的詳細資訊並生成DataFrame
def get_video_details(video_ids):

    video_data = []

    for video_id in video_ids:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        for item in response['items']:
            title = item['snippet']['title']
            publish_date = item['snippet']['publishedAt']
            view_count = item['statistics'].get('viewCount', 0)
            like_count = item['statistics'].get('likeCount', 0)
            dislike_count = item['statistics'].get('dislikeCount', 0)

            video_data.append({
                '影片標題': title,
                '影片ID': video_id,
                '發布日期': publish_date,
                '點閱率': view_count,
                '喜歡數量': like_count,
                '不喜歡數量': dislike_count
            })

    video_df = pd.DataFrame(video_data)
    return video_df


if __name__ == '__main__':
    # 初始化 YouTube API
    api_key = 'YOUR_API_KEY'  # 替換為自己的api key
    youtube = build('youtube', 'v3', developerKey=api_key)

    # 輸入頻道名稱並獲取頻道 ID
    channel_name = "老高與小茉 Mr & Mrs Gao"  # 替換為你要查詢的頻道名稱
    channel_id = check_channel_id(channel_name)

    # 查詢頻道的統計資訊
    check_channel_statistics(channel_id)

    # 下載所有影片封面圖片
    download_all_thumbnails(channel_id)
    
    # 取得影片詳細資訊並顯示
    video_ids = get_all_video_ids(channel_id)
    video_details_df = get_video_details(video_ids)
    print(video_details_df)

    # 把所有影片詳細資訊放入一個csv檔,並創建video_details資料夾來存放檔案
    output_folder = "video_details"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video_details_df.to_csv(os.path.join(output_folder, "video_details.csv"), index=False, encoding='utf-8-sig')
    print("影片資料已儲存至 video_details/video_details.csv")



