import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    a, b, c are points in 3D space (x, y, z)
    Returns angle in degrees
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
    return angle

def run_mediapipe_pose(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*"avc1")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    max_angles = {
        'left_knee': 0,
        'right_knee': 0,
        'left_hip': 0,
        'right_hip': 0,
        'left_ankle': 0,
        'right_ankle': 0,
        'left_shoulder': 0,
        'right_shoulder': 0
    }

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            annotated = frame.copy()
            if results.pose_landmarks:
                # Draw pose landmarks
                mp_drawing.draw_landmarks(
                    annotated,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )
                
                landmarks = results.pose_landmarks.landmark
                
                # Left side points
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                               landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                # Right side points
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                
                # Calculate angles
                left_knee_angle = calculate_angle(left_hip, left_knee, left_ankle)
                right_knee_angle = calculate_angle(right_hip, right_knee, right_ankle)
                left_hip_angle = calculate_angle(left_knee, left_hip, [left_hip[0], left_hip[1] - 1])
                right_hip_angle = calculate_angle(right_knee, right_hip, [right_hip[0], right_hip[1] - 1])
                left_ankle_angle = calculate_angle(left_knee, left_ankle, [left_ankle[0], left_ankle[1] + 1])
                right_ankle_angle = calculate_angle(right_knee, right_ankle, [right_ankle[0], right_ankle[1] + 1])
                left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
                right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
                
                # Update max angles
                max_angles['left_knee'] = max(max_angles['left_knee'], left_knee_angle)
                max_angles['right_knee'] = max(max_angles['right_knee'], right_knee_angle)
                max_angles['left_hip'] = max(max_angles['left_hip'], left_hip_angle)
                max_angles['right_hip'] = max(max_angles['right_hip'], right_hip_angle)
                max_angles['left_ankle'] = max(max_angles['left_ankle'], left_ankle_angle)
                max_angles['right_ankle'] = max(max_angles['right_ankle'], right_ankle_angle)
                max_angles['left_shoulder'] = max(max_angles['left_shoulder'], left_shoulder_angle)
                max_angles['right_shoulder'] = max(max_angles['right_shoulder'], right_shoulder_angle)
                
                # Convert landmark coordinates to pixel coordinates
                def get_pixel_coords(landmark):
                    return (int(landmark[0] * width), int(landmark[1] * height))
                
                # Display angles next to joints
                cv2.putText(annotated, f"{left_knee_angle:.1f}", 
                          get_pixel_coords(left_knee), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{right_knee_angle:.1f}", 
                          get_pixel_coords(right_knee), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{left_hip_angle:.1f}", 
                          get_pixel_coords(left_hip), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{right_hip_angle:.1f}", 
                          get_pixel_coords(right_hip), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{left_ankle_angle:.1f}", 
                          get_pixel_coords(left_ankle), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{right_ankle_angle:.1f}", 
                          get_pixel_coords(right_ankle), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{left_shoulder_angle:.1f}", 
                          get_pixel_coords(left_shoulder), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(annotated, f"{right_shoulder_angle:.1f}", 
                          get_pixel_coords(right_shoulder), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            out.write(annotated)

    cap.release()
    out.release()
    return max_angles