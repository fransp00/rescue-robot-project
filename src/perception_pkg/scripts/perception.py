#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32, Bool
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import mediapipe as mp
import time
from math import ceil

# =====================================================
# INIT ROS
# =====================================================

rospy.init_node("perception_node")

bridge = CvBridge()

# =====================================================
# TOPICS (PUBLISHERS)
# =====================================================

face_pub = rospy.Publisher("/perception/face_count", Int32, queue_size=1)
hand_pub = rospy.Publisher("/perception/hand_count", Int32, queue_size=1)
arm_pub = rospy.Publisher("/perception/arm_count", Int32, queue_size=1)
leg_pub = rospy.Publisher("/perception/leg_count", Int32, queue_size=1)
torso_pub = rospy.Publisher("/perception/torso_count", Int32, queue_size=1)

person_pub = rospy.Publisher("/perception/person_count", Int32, queue_size=1)
human_pub = rospy.Publisher("/perception/human_detected", Bool, queue_size=1)

image_pub = rospy.Publisher("/perception/image", Image, queue_size=1)

# =====================================================
# MEDIAPIPE
# =====================================================

mp_face = mp.solutions.face_detection
mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

face_detector = mp_face.FaceDetection(0.5)

hands_detector = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

pose_detector = mp_pose.Pose(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# =====================================================
# FPS
# =====================================================

last_time = time.time()

# =====================================================
# IMAGE CALLBACK
# =====================================================

def image_callback(msg):

    global last_time

    frame = bridge.imgmsg_to_cv2(msg, "bgr8")
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    h, w, _ = frame.shape

    # =================================================
    # COUNTERS
    # =================================================

    face_count = 0
    hand_count = 0
    arm_count = 0
    leg_count = 0
    torso_count = 0

    # =================================================
    # FACE DETECTION
    # =================================================

    face_results = face_detector.process(rgb)

    if face_results.detections:

        for det in face_results.detections:

            bbox = det.location_data.relative_bounding_box

            x1 = int(bbox.xmin * w)
            y1 = int(bbox.ymin * h)
            x2 = x1 + int(bbox.width * w)
            y2 = y1 + int(bbox.height * h)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(frame, "FACE", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            face_count += 1

    # =================================================
    # HANDS
    # =================================================

    hand_results = hands_detector.process(rgb)

    if hand_results.multi_hand_landmarks:

        for hand_lm in hand_results.multi_hand_landmarks:

            xs = [int(p.x * w) for p in hand_lm.landmark]
            ys = [int(p.y * h) for p in hand_lm.landmark]

            x1, x2 = min(xs), max(xs)
            y1, y2 = min(ys), max(ys)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.putText(frame, "HAND", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)

            hand_count += 1

    # =================================================
    # POSE
    # =================================================

    pose_results = pose_detector.process(rgb)

    if pose_results.pose_landmarks:

        lm = pose_results.pose_landmarks.landmark

        # ---------------- TORSO ----------------
        torso_points = [lm[11], lm[12], lm[23], lm[24]]

        if sum(p.visibility > 0.6 for p in torso_points) >= 3:

            xs = [int(p.x * w) for p in torso_points]
            ys = [int(p.y * h) for p in torso_points]

            x1, x2 = min(xs), max(xs)
            y1, y2 = min(ys), max(ys)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, "TORSO", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

            torso_count += 1

        # ---------------- ARMS ----------------
        arms = [
            [lm[11], lm[13], lm[15]],
            [lm[12], lm[14], lm[16]]
        ]

        for arm in arms:

            if sum(p.visibility > 0.6 for p in arm) >= 2:

                xs = [int(p.x * w) for p in arm]
                ys = [int(p.y * h) for p in arm]

                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, "ARM", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                arm_count += 1

        # ---------------- LEGS ----------------
        legs = [
            [lm[23], lm[25], lm[27]],
            [lm[24], lm[26], lm[28]]
        ]

        for leg in legs:

            if sum(p.visibility > 0.6 for p in leg) >= 2:

                xs = [int(p.x * w) for p in leg]
                ys = [int(p.y * h) for p in leg]

                x1, x2 = min(xs), max(xs)
                y1, y2 = min(ys), max(ys)

                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.putText(frame, "LEG", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

                leg_count += 1

    # =================================================
    # PERSON COUNT LOGIC
    # =================================================

    if face_count > 0:
        person_count = max(face_count, ceil(hand_count / 2))
    elif hand_count > 0:
        person_count = ceil(hand_count / 2)
    elif torso_count > 0:
        person_count = 1
    elif arm_count > 0:
        person_count = 1
    elif leg_count > 0:
        person_count = 1
    else:
        person_count = 0

    human_detected = person_count > 0

    # =================================================
    # PUBLISH COUNTS
    # =================================================

    face_pub.publish(face_count)
    hand_pub.publish(hand_count)
    arm_pub.publish(arm_count)
    leg_pub.publish(leg_count)
    torso_pub.publish(torso_count)

    person_pub.publish(person_count)
    human_pub.publish(human_detected)

    # =================================================
    # FPS
    # =================================================

    current_time = time.time()
    fps = 1.0 / (current_time - last_time)
    last_time = current_time

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame, f"People: {person_count}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # =================================================
    # PUBLISH IMAGE
    # =================================================

    img_msg = bridge.cv2_to_imgmsg(frame, "bgr8")
    image_pub.publish(img_msg)

    cv2.imshow("Perception", frame)
    cv2.waitKey(1)

# =====================================================
# SUBSCRIBER
# =====================================================

rospy.Subscriber(
    "/usb_cam/image_raw",
    Image,
    image_callback,
    queue_size=1
)

rospy.loginfo("Perception node running...")
rospy.spin()