
import math


def distance(p1, p2):
    """Calculate the distance between two hand landmarks."""
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def finger_extended(hand_landmarks, tip_id, pip_id):
    """
    Check whether a finger is extended.
    Works best when the palm faces the camera.
    """
    lm = hand_landmarks.landmark
    return lm[tip_id].y < lm[pip_id].y


def finger_folded(hand_landmarks, tip_id, pip_id):
    """Check whether a finger is folded."""
    return not finger_extended(hand_landmarks, tip_id, pip_id)


def thumb_is_up(hand_landmarks):
    lm = hand_landmarks.landmark

    # Compare thumb tip and thumb joint distances from the thumb base.
    tip_distance = distance(lm[4], lm[5])
    joint_distance = distance(lm[3], lm[5])

    return tip_distance > joint_distance + 0.02


def thumb_is_down(hand_landmarks):
    lm = hand_landmarks.landmark

    # Thumb tip is below its joint in the camera image.
    return lm[4].y > lm[3].y + 0.025


def get_finger_states(hand_landmarks):
    """Return index, middle, ring and pinky extension states."""
    return (
        finger_extended(hand_landmarks, 8, 6),
        finger_extended(hand_landmarks, 12, 10),
        finger_extended(hand_landmarks, 16, 14),
        finger_extended(hand_landmarks, 20, 18),
    )


def is_index_only(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        index
        and not middle
        and not ring
        and not pinky
        and not thumb_is_up(hand_landmarks)
    )


def is_two_fingers(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return index and middle and not ring and not pinky


def is_open_palm(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        index
        and middle
        and ring
        and pinky
        and thumb_is_up(hand_landmarks)
    )


def is_fist(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        not index
        and not middle
        and not ring
        and not pinky
        and not thumb_is_up(hand_landmarks)
    )


def is_pinky_only(hand_landmarks):
    """
    Right-click only if the pinky is extended and the other
    three fingers are folded.
    """
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        not index
        and not middle
        and not ring
        and pinky
    )


def is_thumb_only(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        thumb_is_up(hand_landmarks)
        and not index
        and not middle
        and not ring
        and not pinky
    )


def is_thumb_down_only(hand_landmarks):
    index, middle, ring, pinky = get_finger_states(hand_landmarks)

    return (
        thumb_is_down(hand_landmarks)
        and not index
        and not middle
        and not ring
        and not pinky
    )


def is_pinch(hand_landmarks):
    """Detect a pinch between thumb and index fingertip."""
    lm = hand_landmarks.landmark

    return distance(lm[4], lm[8]) < 0.045


def is_both_thumbs_down(hand_list):
    """True only when both detected hands show thumbs down."""
    if len(hand_list) != 2:
        return False

    return all(is_thumb_down_only(hand) for hand in hand_list)


def is_two_index_fingers(hand_list):
    """True when both hands show index finger only."""
    if len(hand_list) != 2:
        return False

    return all(is_index_only(hand) for hand in hand_list)

