
import math


# --------------------------------------------------
# BASIC LANDMARK FUNCTIONS
# --------------------------------------------------

def distance(p1, p2):
    """Calculate the distance between two landmarks."""
    return math.hypot(
        p1.x - p2.x,
        p1.y - p2.y
    )


def finger_extended(hand, tip_id, pip_id):
    """
    Detect an extended finger.
    Best results occur when the palm faces the webcam.
    """
    lm = hand.landmark
    return lm[tip_id].y < lm[pip_id].y


def finger_folded(hand, tip_id, pip_id):
    """Detect a folded finger."""
    return not finger_extended(hand, tip_id, pip_id)


def get_finger_states(hand):
    """
    Return the states of index, middle, ring and pinky.
    True = extended; False = folded.
    """
    return (
        finger_extended(hand, 8, 6),
        finger_extended(hand, 12, 10),
        finger_extended(hand, 16, 14),
        finger_extended(hand, 20, 18),
    )


# --------------------------------------------------
# THUMB DETECTION
# --------------------------------------------------

def thumb_is_up(hand):
    lm = hand.landmark

    tip_distance = distance(lm[4], lm[5])
    joint_distance = distance(lm[3], lm[5])

    return tip_distance > joint_distance + 0.02


def thumb_is_down(hand):
    lm = hand.landmark

    # Thumb tip must be below the thumb joint in the image.
    return lm[4].y > lm[3].y + 0.025


# --------------------------------------------------
# ONE-HAND GESTURES
# --------------------------------------------------

def is_index_only(hand):
    """
    Index finger extended; middle, ring and pinky folded.
    Thumb must not be extended.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        index
        and not middle
        and not ring
        and not pinky
        and not thumb_is_up(hand)
    )


def is_two_fingers(hand):
    """
    Index + middle extended.
    Ring and pinky folded.
    Used for continuous scrolling up.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        index
        and middle
        and not ring
        and not pinky
    )


def is_thumb_only(hand):
    """
    Thumb extended, with all four fingers folded.
    Used for continuous scrolling down.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        thumb_is_up(hand)
        and not thumb_is_down(hand)
        and not index
        and not middle
        and not ring
        and not pinky
    )


def is_thumb_down_only(hand):
    """
    Thumb pointing down, with all four fingers folded.
    Used by the two-hand volume-down gesture.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        thumb_is_down(hand)
        and not index
        and not middle
        and not ring
        and not pinky
    )


def is_both_thumbs_down(hand_list):
    """Both hands must independently satisfy thumbs-down."""
    if len(hand_list) != 2:
        return False

    return all(is_thumb_down_only(hand) for hand in hand_list)


def is_two_index_fingers(hand_list):
    """Both hands show index finger only."""
    if len(hand_list) != 2:
        return False

    return all(is_index_only(hand) for hand in hand_list)


def is_pinky_only(hand):
    """
    Right-click only for pinky-only.
    Ring finger MUST be folded.
    Pinky + ring extended is NOT pinky-only.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        not index
        and not middle
        and not ring
        and pinky
    )


def is_open_palm(hand):
    """All four fingers and thumb extended."""
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        index
        and middle
        and ring
        and pinky
        and thumb_is_up(hand)
    )


def is_fist(hand):
    """All four fingers folded and thumb not extended."""
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        not index
        and not middle
        and not ring
        and not pinky
        and not thumb_is_up(hand)
    )


def is_pinch(hand):
    """Thumb and index fingertips close together."""
    lm = hand.landmark

    return distance(lm[4], lm[8]) < 0.045


# --------------------------------------------------
# DEBUG INFORMATION FOR WEBCAM
# --------------------------------------------------

def get_finger_debug_text(hand):
    """
    Return finger states for displaying on the webcam.
    1 = extended, 0 = folded.
    """
    index, middle, ring, pinky = get_finger_states(hand)

    return (
        f"I:{int(index)} "
        f"M:{int(middle)} "
        f"R:{int(ring)} "
        f"P:{int(pinky)}"
    )

