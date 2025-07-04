#import and object creations
import mediapipe as mp
import numpy as np
import json

mp_drawing = mp.solutions.drawing_utils #for drawing in frames
mp_pose = mp.solutions.pose             #for pose estimations

# dictionary for body parts (points: dic)
points = {
     'nose': 0, 
     'left_eye_inner': 1, 
     'left_eye': 2, 
     'left_eye_outer': 3, 
     'right_eye_inner': 4, 
     'right_eye': 5, 
     'right_eye_outer': 6, 
     'left_ear': 7, 
     'right_ear': 8, 
     'mouth_left': 9, 
     'mouth_right': 10, 
     'left_shoulder': 11, 
     'right_shoulder': 12,
     'left_elbow': 13, 
     'right_elbow': 14, 
     'left_wrist': 15, 
     'right_wrist': 16, 
     'left_pinky': 17, 
     'right_pinky': 18, 
     'left_index': 19, 
     'right_index': 20, 
     'left_thumb': 21, 
     'right_thumb': 22, 
     'left_hip': 23, 
     'right_hip': 24, 
     'left_knee': 25, 
     'right_knee': 26, 
     'left_ankle': 27, 
     'right_ankle': 28, 
     'left_heel': 29, 
     'right_heel': 30, 
     'left_foot_index': 31, 
     'right_foot_index': 32
     }

#to find the angles using coodinates (calAngle : funtion)
def calAngle(a1,b1,c1):
    a = np.array(a1)
    b = np.array(b1)
    c = np.array(c1)

    '''
    a,b and c are points in space with x,y and z axis and 
    rad = tan(c(y)-b(y), c(x)-b(x)) - tan(a(y)-b(y),a(x)-b(x))
    '''
    rad = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(rad*180.0/np.pi)

    return angle


def somefuntion(landmarks):                       
    angle_data = []
    #landmarks = Show_pos_estimatiom(filePath)

    try:
        #left elbow
        a = landmarks[points['left_shoulder']].x,landmarks[points['left_shoulder']].y
        b = landmarks[points['left_elbow']].x,landmarks[points['left_elbow']].y
        c = landmarks[points['left_wrist']].x,landmarks[points['left_wrist']].y
        left_elbow = calAngle(a,b,c) 

        #right elbow
        a = landmarks[points['right_shoulder']].x,landmarks[points['right_shoulder']].y
        b = landmarks[points['right_elbow']].x,landmarks[points['right_elbow']].y
        c = landmarks[points['right_wrist']].x,landmarks[points['right_wrist']].y
        right_elbow = calAngle(a,b,c)

        #right knee 
        a = landmarks[points['right_ankle']].x,landmarks[points['right_ankle']].y
        b = landmarks[points['right_knee']].x,landmarks[points['right_knee']].y
        c = landmarks[points['right_hip']].x,landmarks[points['right_hip']].y
        right_knee = calAngle(a,b,c)

        #left knee 
        a = landmarks[points['left_ankle']].x,landmarks[points['left_ankle']].y
        b = landmarks[points['left_knee']].x,landmarks[points['left_knee']].y
        c = landmarks[points['left_hip']].x,landmarks[points['left_hip']].y
        left_knee = calAngle(a,b,c)

        #right shoulder 
        a = landmarks[points['right_elbow']].x,landmarks[points['right_elbow']].y
        b = landmarks[points['right_shoulder']].x,landmarks[points['right_shoulder']].y
        c = landmarks[points['right_hip']].x,landmarks[points['right_hip']].y
        right_shoulder = calAngle(a,b,c)    

        #left shoulder
        a = landmarks[points['left_elbow']].x,landmarks[points['left_elbow']].y
        b = landmarks[points['left_shoulder']].x,landmarks[points['left_shoulder']].y
        c = landmarks[points['left_hip']].x,landmarks[points['left_hip']].y
        left_shoulder = calAngle(a,b,c)

        #left hip
        a = landmarks[points['left_knee']].x,landmarks[points['left_knee']].y
        b = landmarks[points['left_hip']].x,landmarks[points['left_hip']].y
        c = landmarks[points['left_shoulder']].x,landmarks[points['left_shoulder']].y
        left_hip = calAngle(a,b,c)

        #right hip
        a = landmarks[points['right_knee']].x,landmarks[points['right_knee']].y
        b = landmarks[points['right_hip']].x,landmarks[points['right_hip']].y
        c = landmarks[points['right_shoulder']].x,landmarks[points['right_shoulder']].y
        right_hip = calAngle(a,b,c)

        angle_data = [
            left_elbow,
            right_elbow,
            right_knee,
            left_knee,
            right_shoulder,
            left_shoulder,
            left_hip,
            right_hip
        ]
    except Exception as e:
        print(f'error: {e} ')
        
    return angle_data


#main class
class MatchYogaPos:

    def __init__(self):
        with open('C:\\Users\\katti\\detection-yoga\\poses_data.json', 'r') as json_file:
            poses_data = json.load(json_file)
        
        self.angle_list = poses_data
    
    def _compare(self,angles:list,refAngles:list):
        
        err = 30
        t1 = angles
        angles.sort()
        refAngles.sort()
        ret_list = [True,-1,-1]


        if abs(angles[0]-refAngles[0]) < err and abs(angles[1]-refAngles[1]) < err:
            return ret_list
        else:
            ret_list[0] =  False
            if t1 == angles:
                
                ret_list[1] = abs(angles[0]-refAngles[0])
                ret_list[2] = abs(angles[1]-refAngles[1])
            else:
                
                ret_list[2] = abs(angles[0]-refAngles[0])
                ret_list[1] = abs(angles[1]-refAngles[1])

            return ret_list

    def matchYogaPos(self,img_landmarks,posName):
        
        ref_angles = self.angle_list[posName]
        angles = somefuntion(img_landmarks)
        bool_list = []
        bool_list.append(self._compare([angles[0],angles[1]],[ref_angles[0],ref_angles[1]]))
        bool_list.append(self._compare([angles[2],angles[3]],[ref_angles[2],ref_angles[3]]))
        bool_list.append(self._compare([angles[4],angles[5]],[ref_angles[4],ref_angles[5]])) 
        bool_list.append(self._compare([angles[6],angles[7]],[ref_angles[6],ref_angles[7]]))

        return bool_list