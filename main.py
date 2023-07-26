# 左右の動作の検知と上への動作を検知できるようにしました。
import cv2
import mediapipe as mp
import math
import json

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
gosa = 0.15#動きの判定を調整する変数(基本)
up = 0.3#動きの判定の調整(上の判定時に使用)
# VideoCaptureオブジェクトを取得します
cap = cv2.VideoCapture(0)

# 左手と右手の前フレームのx座標を保存する変数
prev_x_right = None
prev_x_left = None
prev_y_right = None
prev_y_left = None

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                # 手が右手か左手かを判断します
                if hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x:
                    current_x_right = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                    current_y_right = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

                   
                    if prev_x_right is not None:
                        # 前フレームのx座標と現フレームのx座標を比較します
                        if current_x_right > prev_x_right + gosa:
                            print('右手が右に移動')
                            data = {"judge" : 1}
                            json_data = json.dumps(data)
                            print(json_data)
                        
                        elif current_x_right + gosa < prev_x_right:
                            print('右手が左に移動')
                            data = {"judge" : 2}
                            json_data = json.dumps(data)
                            print(json_data)
                        
                         # 親指と人差し指の先端間の距離を計算します
                        distance = math.sqrt((thumb_tip.x - index_finger_tip.x)**2 +
                                         (thumb_tip.y - index_finger_tip.y)**2)

                        # 距離が一定の閾値（ここでは0.1とします）以下であれば、手が握られていると判断します
                        if distance < 0.1:
                            print("右の手を握りました")
                            data = {"judge" : 0}
                            json_data = json.dumps(data)
                            print(json_data)
                        
                        else:
                            print('右手が停止しています')
                        
                        if prev_y_right is not None:
                            # 前フレームのy座標と現フレームのy座標を比較します
                            if current_y_right + gosa + up < prev_y_right:
                                print('右手が上に移動')
                                data = {"judge" : 3}
                                json_data = json.dumps(data)
                                print(json_data)
                                
                        prev_y_right = current_y_right
                    prev_x_right = current_x_right
                    
                else:
                    current_x_left = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                    current_y_left = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
                    if prev_x_left is not None:
                        # 前フレームのx座標と現フレームのx座標を比較します
                        if current_x_left > prev_x_left + gosa:
                            print('左手が右に移動')
                            data = {"judge" : 1}
                            json_data = json.dumps(data)
                            print(json_data)
                        
                        elif current_x_left + gosa < prev_x_left:
                            print('左手が左に移動')
                            data = {"judge" : 2}
                            json_data = json.dumps(data)
                            print(json_data)
                            
                        distance = math.sqrt((thumb_tip.x - index_finger_tip.x)**2 +
                                         (thumb_tip.y - index_finger_tip.y)**2)

                        # 距離が一定の閾値（ここでは0.1とします）以下であれば、手が握られていると判断します
                        if distance < 0.1:
                            print("左の手を握りました")
                            data = {"judge" : 0}
                            json_data = json.dumps(data)
                            print(json_data)
                        
                        else:
                            print('左手が停止しています')
                        if prev_y_left is not None:
                            # 前フレームのy座標と現フレームのy座標を比較します
                            if current_y_left + gosa + up < prev_y_left:
                                print('左手が上に移動')
                                data = {"judge" : 3}
                                json_data = json.dumps(data)
                                print(json_data)
                                
                        prev_y_left = current_y_left
                    prev_x_left = current_x_left

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
