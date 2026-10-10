
import cv2
import mediapipe as mp
import pyautogui
import time

from gesture import (
    is_index_only,
    is_two_fingers,
    is_open_palm,
    is_fist,
    is_pinky_only,
    is_thumb_only,
    is_both_thumbs_down,
    is_two_index_fingers,
    is_pinch,
)

# ---------------- CONFIGURATION ----------------

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540

# Cursor smoothing: lower = smoother, higher = faster.
SMOOTHING = 0.30

# Continuous volume control interval in seconds.
VOLUME_INTERVAL = 0.12

# Minimum time between click and media actions.
ACTION_DELAY = 0.40

# Scroll amount per frame.
SCROLL_AMOUNT = 1

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    raise SystemExit

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
)

previous_x = SCREEN_WIDTH // 2
previous_y = SCREEN_HEIGHT // 2

last_volume_time = 0
last_action_time = 0

dragging = False
previous_gesture = ""

# ---------------- MAIN LOOP ----------------

try:
    while True:
        success, frame = cap.read()

        if not success:
            print("ERROR: Unable to read webcam frame.")
            break

        # Mirror the camera image.
        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        hand_list = results.multi_hand_landmarks or []
        gesture_name = "No gesture"

        # Draw detected hands.
        for hand_landmarks in hand_list:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

        current_time = time.time()

        # ------------------------------------------------
        # PRIORITY 1: TWO-HAND GESTURES
        # ------------------------------------------------

        if len(hand_list) == 2:

            # Both thumbs down: continuously decrease volume.
            if is_both_thumbs_down(hand_list):
                gesture_name = "BOTH THUMBS DOWN - VOLUME DOWN"

                if current_time - last_volume_time >= VOLUME_INTERVAL:
                    pyautogui.press("volumedown")
                    last_volume_time = current_time

            # Both index fingers only: continuously increase volume.
            elif is_two_index_fingers(hand_list):
                gesture_name = "BOTH INDEX FINGERS - VOLUME UP"

                if current_time - last_volume_time >= VOLUME_INTERVAL:
                    pyautogui.press("volumeup")
                    last_volume_time = current_time

            else:
                # Two hands detected, but no matching two-hand gesture.
                # Suppress one-hand cursor, click and scroll controls.
                gesture_name = "Two hands detected - waiting"

        # ------------------------------------------------
        # PRIORITY 2: ONE-HAND GESTURES
        # ------------------------------------------------

        elif len(hand_list) == 1:
            hand = hand_list[0]
            lm = hand.landmark

            # 1. Index finger only: move cursor.
            if is_index_only(hand):
                gesture_name = "INDEX ONLY - MOVE CURSOR"

                target_x = int(lm[8].x * SCREEN_WIDTH)
                target_y = int(lm[8].y * SCREEN_HEIGHT)

                target_x = max(0, min(SCREEN_WIDTH - 1, target_x))
                target_y = max(0, min(SCREEN_HEIGHT - 1, target_y))

                smooth_x = (
                    previous_x
                    + (target_x - previous_x) * SMOOTHING
                )

                smooth_y = (
                    previous_y
                    + (target_y - previous_y) * SMOOTHING
                )

                previous_x = int(smooth_x)
                previous_y = int(smooth_y)

                pyautogui.moveTo(previous_x, previous_y)

            # 2. Pinch: left-click.
            # Check before scroll and other gestures.
            elif is_pinch(hand):
                gesture_name = "PINCH - LEFT CLICK"

                if (
                    current_time - last_action_time >= ACTION_DELAY
                    and previous_gesture != "PINCH - LEFT CLICK"
                ):
                    pyautogui.click()
                    last_action_time = current_time

            # 3. Pinky only: right-click.
            elif is_pinky_only(hand):
                gesture_name = "PINKY ONLY - RIGHT CLICK"

                if (
                    current_time - last_action_time >= ACTION_DELAY
                    and previous_gesture != "PINKY ONLY - RIGHT CLICK"
                ):
                    pyautogui.rightClick()
                    last_action_time = current_time

            # 4. Two fingers: scroll up.
            elif is_two_fingers(hand):
                gesture_name = "TWO FINGERS - SCROLL UP"
                pyautogui.scroll(SCROLL_AMOUNT)

            # 5. Fist: drag.
            elif is_fist(hand):
                gesture_name = "FIST - DRAG"

                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True

            # 6. Open palm: play/pause.
            elif is_open_palm(hand):
                gesture_name = "OPEN PALM - PLAY/PAUSE"

                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

                if (
                    current_time - last_action_time >= ACTION_DELAY
                    and previous_gesture != "OPEN PALM - PLAY/PAUSE"
                ):
                    pyautogui.press("playpause")
                    last_action_time = current_time

            # 7. Other poses: no action.
            else:
                gesture_name = "Gesture not recognized"

                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

        # ------------------------------------------------
        # NO HANDS DETECTED
        # ------------------------------------------------

        else:
            gesture_name = "No hand detected"

            if dragging:
                pyautogui.mouseUp()
                dragging = False

        # Release drag if the drag pose ends.
        if dragging and gesture_name != "FIST - DRAG":
            pyautogui.mouseUp()
            dragging = False

        previous_gesture = gesture_name

        # ------------------------------------------------
        # DISPLAY
        # ------------------------------------------------

        cv2.putText(
            frame,
            gesture_name,
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            "Q = Quit",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        cv2.imshow("Hand Gesture Control", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

finally:
    if dragging:
        pyautogui.mouseUp()

    cap.release()
    hands.close()
    cv2.destroyAllWindows()

