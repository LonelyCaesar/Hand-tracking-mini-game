import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0) # 電腦的攝影機
#設置畫面的大小
cap.set(3,1280)
cap.set(4,720)

imgDesk = cv2.imread('puck/desk.png')
imgBall = cv2.imread('puck/ball.png', cv2.IMREAD_UNCHANGED)
imgBlock1 = cv2.imread('puck/block1.png', cv2.IMREAD_UNCHANGED)
imgBlock2 = cv2.imread('puck/block2.png', cv2.IMREAD_UNCHANGED)

imgDesk = cv2.resize(imgDesk, dsize=(1280, 720))

imgBlock1 = cv2.resize(imgBlock1, dsize=(50,200))
imgBlock2 = cv2.resize(imgBlock2, dsize=(50,200))

detector = HandDetector(detectionCon=0.8, maxHands=2)

ballpos = [100, 100]

speedx, speedy = 10, 10

gameover = False

score = [0, 0]

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    img = cv2.addWeighted(img, 0.4, imgDesk, 0.6, 0)

    if hands:
        for hand in hands:
            x, y, z =hand['lmList'][8]
            h1, w1 = imgBlock1.shape[0:2]
            y1 = y - h1 // 2

            if hand['type'] == 'Left':
                img = cvzone.overlayPNG(img, imgBlock1, (40, y1))
                if 40 < ballpos[0] < 40 + w1 and y1 < ballpos[1] < y1 + h1:
                    speedx = -speedx
                    score[0] += 1


            if hand['type'] == 'Right':
                img = cvzone.overlayPNG(img, imgBlock2,(1180,y1))
                if 1080 < ballpos[0] < 1080 + w1 and y1 < ballpos[1] < y1 + h1:
                    speedx = -speedx
                    score[1] += 1
    if ballpos[0] < 50 or ballpos[0] > 1150:
        gameover = True

    if gameover is True:
        cvzone.putTextRect(img, "Game Over", [300, 300],scale=7, thickness=5, offset=20)
        cvzone.putTextRect(img, f'Left:{score[0]} and Right:{score[1]}', [100, 500],scale=7, thickness=5, offset=20)

    else:
        if ballpos[1] >= 600 or ballpos[1] <= 50:
            speedy = -speedy
    # 球的x和y坐標
    ballpos[0] = ballpos[0] + speedx
    ballpos[1] = ballpos[1] + speedy
    # 桌球圖片、將imgBall放在球桌img的固定坐標位置
    img = cvzone.overlayPNG(img, imgBall, ballpos)
    # 顯示計分板
    cvzone.putTextRect(img, f'Left:{score[0]} and Right:{score[1]}', (400, 710))

    cv2.imshow("image", img)
    key = cv2.waitKey(1)
    # 按下‘q'重新開始遊戲
    if key == ord('q'):
        ballpos = [100, 100]
        speedx, speedy = 10, 10
        gameover = False
        score = [0, 0]

    if key & 0xFF == 27:  # 按下 Esc 鍵停止
        break
#釋放頻資源
cap.release()
cv2.destroyAllWindows()