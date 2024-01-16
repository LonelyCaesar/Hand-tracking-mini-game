# 手勢追蹤小遊戲
# 一、說明
本專題使用anaconda3.9以上版本、mediapipg、openCV製作出貪吃蛇小遊戲、桌上撞球的互動小遊戲。

套件安裝準備：
Jupyter 本身是一個 Python 的編輯環境，如果直接安裝 mediapipe 可能會導致運作時互相衝突，因此需要先安裝 mediapipe 的虛擬環境，在上面安裝 mediapipe 後就能正常運行。
1.	請到anaconda官方網站下載軟體，到桌面開啟cmd執行conda create --name mediapipe python=3.9。
2.	輸入conda activate mediapipe或pip install mediapipe指令安裝套件。
3.	輸入pip install tensorflow指令安裝套件。
4.	輸入pip install opencv-python指令安裝套件。
5.	輸入pip install cvzone指令安裝套件。
# 二、相關文章
使用 MediaPipe進行手掌的偵測，再透過 OpenCV 讀取攝影鏡頭影像進行辨識，在手掌與每隻手指標記骨架。

MediaPipe Hands 利用多個模型協同工作，可以偵測手掌模型，返回手掌與每隻手指精確的 3D 關鍵點，MediaPipe Hand 除了可以偵測清晰的手掌形狀與動作，更可以判斷出被少部分被遮蔽的手指形狀和動作，再清晰的畫面下，針對手掌判斷的精準度可達 95.7%。

Mediapipe 偵測手掌後，會在手掌與手指上產生 21 個具有 x、y、z 座標的節點，透過包含立體深度的節點，就能在 3D 場景中做出多種不同的應用，下圖標示出每個節點的順序和位置。

如果同時出現兩隻手，採用交錯偵測 ( 短時間內偵測兩次，一次偵測一隻手 )，最後仍然維持 21 個點的數據，如果只希望偵測一隻手，可設定 max_num_hands=1。

參考網址：
