import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class heatMap:
    
    def createHeatmap(self,difList):

        body_parts = ["Left Elbow", "Right Elbow", "right knee", "left knee", "right shoulder", "left shoulder", "left hip", "right hip"]
        
        angle_differences = []
        for angles in difList:
            if angles[0] == True:
                angle_differences.append(0)
                angle_differences.append(0)
            else:
                angle_differences.append(angles[1])
                angle_differences.append(angles[2])

        angle_differences = np.array(angle_differences)
        heatmap_data = angle_differences.reshape(1, -1)


        sns.heatmap(heatmap_data, annot=True, cmap= "Greens", xticklabels=body_parts, yticklabels=False)


        plt.xlabel("Body Parts")
        plt.ylabel("Difference in Angles")
        plt.title(f"Angle Differences for Yoga Pose ")

        plt.show()
