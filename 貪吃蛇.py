import math
import random
import cv2
import cvzone
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0) # 電腦的攝影機
#設置畫面的大小
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] # 蛇身上所有的點
        self.lengths = [] # 不同點之間距離
        self.currentLength = 0 # 當前蛇的長度
        self.allowedLength = 150 # 最大允許長度
        self.previousHead = 0, 0 # 先前蛇的頭部
        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(100, 1000), random.randint(100, 600)

    def update(self, imgMain, currentHead):  # 實例方法
        # 遊戲結束，打印腳本
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [370, 350],
                               scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score:{self.score}', [300, 500],
                               scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead
            self.points.append([cx, cy])  # 蛇的點列表節點
            distance = math.hypot(cx - px, cy - py)  # 兩點之間的距離
            self.lengths.append(distance)  # 蛇的距離列表內容
            self.currentLength += distance
            self.previousHead = cx, cy

            # 長度縮小
            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break
            # 檢查貪吃蛇是否碰觸到食物
            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            # 使用線條繪製貪吃蛇
            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (128, 255, 255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (128, 128, 255), cv2.FILLED)

            # 顯示食物
            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,
                                        (rx - self.wFood // 2, ry - self.hFood // 2))

            cvzone.putTextRect(imgMain, f'Your Score:{self.score}', [50, 80],
                               scale=3, thickness=5, offset=10)
            # 檢測是否碰撞
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 0, 255), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                print("Hit")
                self.gameOver = True
                self.points = []  # 蛇身上所有的點
                self.lengths = []  # 不同點之間距離
                self.currentLength = 0  # 當前蛇的長度
                self.allowedLength = 150  # 最大允許長度
                self.previousHead = 0, 0  # 先前蛇的頭部
                self.randomFoodLocation()
        return imgMain


game = SnakeGameClass("snake\dd.png")
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1) # 鏡像翻轉
    hands, img = detector.findHands(img, flipType=False)
    # 檢測到第一個手，標記手部位置
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]  # 只要食指指尖的x和y坐標
        img = game.update(img, pointIndex)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    # 按下‘q'重新開始遊戲
    if key == ord('q'):
        game.gameOver = False
        game.score = 0
        game.points = []  # 蛇身上所有的點
        game.lengths = []  # 不同點之間距離
        game.currentLength = 0  # 當前蛇的長度
        game.allowedLength = 150  # 最大允許長度
        game.previousHead = (0, 0)  # 先前蛇的頭部
        game.randomFoodLocation()
    if key & 0xFF == 27:  # 按下 Esc 鍵停止
        break
#釋放頻資源
cap.release()
cv2.destroyAllWindows()