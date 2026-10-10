
import cv2
import mediapipe as mp
import pyautogui
import time

from gesture import (
    is_index_only,
    is_two_fingers,
    is_thumb_only,
    is_open_palm,
    is_fist,
    is_pinky_only,
    is_pinch,
    is_both_thumbs_down,
    is_two_index_fingers,
    get_finger_debug_text,
)


# ==================================================
# CONFIGURATION
# ==================================================

CAMERA_INDEX = 0

CAMERA_WIDTH = 960
CAMERA_HEIGHT = 540

SMOOTHING = 0.35

# Repeat volume commands while the gesture is held.
VOLUME_INTERVAL = 0.15

# Delay between scroll commands.
SCROLL_INTERVAL = 0.08
SCROLL_AMOUNT = 2

# Click/media action cooldown.
ACTION_COOLDOWN = 0.45

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


# ==================================================
# MEDIAPIPE AND CAMERA SETUP
# ==================================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

camera = cv2.VideoCapture(CAMERA_INDEX)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)

if not camera.isOpened():
    print("ERROR: Could not open webcam.")
    print("Check whether another application is using your camera.")
    raise SystemExit


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65,
)


# ==================================================
# STATE VARIABLES
# ==================================================

previous_x = SCREEN_WIDTH // 2
previous_y = SCREEN_HEIGHT // 2

last_volume_time = 0
last_scroll_time = 0
last_action_time = 0

previous_gesture = ""
dragging = False


# ==================================================
# MAIN LOOP
# ==================================================

try:
    while True:

        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read webcam frame.")
            break

        # Mirror image for natural movement.
        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb_frame)

        hand_list = (
            results.multi_hand_landmarks
            if results.multi_hand_landmarks
            else []
        )

        current_time = time.time()
        gesture_name = "No hand detected"
        debug_text = ""

        # Draw hand landmarks.
        for hand in hand_list:
            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

        # ==================================================
        # PRIORITY 1: TWO-HAND GESTURES
        # ==================================================

        if len(hand_list) == 2:

            if is_both_thumbs_down(hand_list):

                gesture_name = "BOTH THUMBS DOWN: VOLUME DOWN"

                # Repeatedly decrease volume while held.
                if current_time - last_volume_time >= VOLUME_INTERVAL:
                    pyautogui.press("volumedown")
                    last_volume_time = current_time

            elif is_two_index_fingers(hand_list):

                gesture_name = "TWO INDEX FINGERS: VOLUME UP"

                # Repeatedly increase volume while held.
                if current_time - last_volume_time >= VOLUME_INTERVAL:
                    pyautogui.press("volumeup")
                    last_volume_time = current_time

            else:

                # Suppress single-hand controls when two hands
                # are present, preventing accidental scrolling.
                gesture_name = "Two hands detected"

        # ==================================================
        # PRIORITY 2: ONE-HAND GESTURES
        # ==================================================

        elif len(hand_list) == 1:

            hand = hand_list[0]
            lm = hand.landmark

            debug_text = get_finger_debug_text(hand)

            # ----------------------------------------------
            # 1. TWO FINGERS: SCROLL UP
            # ----------------------------------------------

            if is_two_fingers(hand):

                gesture_name = "TWO FINGERS: SCROLL UP"

                if current_time - last_scroll_time >= SCROLL_INTERVAL:
                    pyautogui.scroll(SCROLL_AMOUNT)
                    last_scroll_time = current_time

            # ----------------------------------------------
            # 2. THUMB ONLY: SCROLL DOWN
            # ----------------------------------------------

            elif is_thumb_only(hand):

                gesture_name = "THUMB ONLY: SCROLL DOWN"

                if current_time - last_scroll_time >= SCROLL_INTERVAL:
                    pyautogui.scroll(-SCROLL_AMOUNT)
                    last_scroll_time = current_time

            # ----------------------------------------------
            # 3. INDEX ONLY: MOVE CURSOR
            # ----------------------------------------------

            elif is_index_only(hand):

                gesture_name = "INDEX ONLY: MOVE CURSOR"

                target_x = int(lm[8].x * SCREEN_WIDTH)
                target_y = int(lm[8].y * SCREEN_HEIGHT)

                target_x = max(
                    0,
                    min(SCREEN_WIDTH - 1, target_x)
                )

                target_y = max(
                    0,
                    min(SCREEN_HEIGHT - 1, target_y)
                )

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

                pyautogui.moveTo(
                    previous_x,
                    previous_y
                )

            # ----------------------------------------------
            # 4. PINKY ONLY: RIGHT CLICK
            # ----------------------------------------------

            elif is_pinky_only(hand):

                gesture_name = "PINKY ONLY: RIGHT CLICK"

                if (
                    gesture_name != previous_gesture
                    and current_time - last_action_time >= ACTION_COOLDOWN
                ):
                    pyautogui.rightClick()
                    last_action_time = current_time

            # ----------------------------------------------
            # 5. FIST: DRAG
            # ----------------------------------------------

            elif is_fist(hand):

                gesture_name = "FIST: DRAG"

                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True

            # ----------------------------------------------
            # 6. OPEN PALM: PLAY/PAUSE
            # ----------------------------------------------

            elif is_open_palm(hand):

                gesture_name = "OPEN PALM: PLAY/PAUSE"

                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

                if (
                    gesture_name != previous_gesture
                    and current_time - last_action_time >= ACTION_COOLDOWN
                ):
                    pyautogui.press("playpause")
                    last_action_time = current_time

            # ----------------------------------------------
            # 7. PINCH: LEFT CLICK
            # ----------------------------------------------

            elif is_pinch(hand):

                gesture_name = "PINCH: LEFT CLICK"

                if (
                    gesture_name != previous_gesture
                    and current_time - last_action_time >= ACTION_COOLDOWN
                ):
                    pyautogui.click()
                    last_action_time = current_time

            # ----------------------------------------------
            # 8. UNKNOWN GESTURE
            # ----------------------------------------------

            else:

                gesture_name = "Gesture not recognized"

        # ==================================================
        # NO HANDS DETECTED
        # ==================================================

        else:

            gesture_name = "No hand detected"

        # ==================================================
        # DRAG RELEASE
        # ==================================================

        if dragging and gesture_name != "FIST: DRAG":
            pyautogui.mouseUp()
            dragging = False

        previous_gesture = gesture_name

        # ==================================================
        # WEBCAM DISPLAY
        # ==================================================

        cv2.putText(
            frame,
            gesture_name,
            (10, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 255, 0),
            2
        )

        if debug_text:
            cv2.putText(
                frame,
                debug_text,
                (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

        cv2.putText(
            frame,
            "Q = Quit",
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AirControlAI - Hand Gesture Control",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break


# ==================================================
# CLEANUP
# ==================================================

finally:

    if dragging:
        pyautogui.mouseUp()

    camera.release()
    hands.close()
    cv2.destroyAllWindows()

