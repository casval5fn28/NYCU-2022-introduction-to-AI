import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    """
            First create an array for dataset and get paths of "face" and 
        "non-face" , then read the images as grayscale . For "face" , label 
        it as "1" while labeling "non-face" as "0" .
            Finally , add the images' numpy array and label into "dataset"
        and return "dataset"
    """
    dataset = []
    isFace = dataPath + '/face'
    notFace = dataPath + '/non-face'
    L1 = os.listdir(isFace)
    L2 = os.listdir(notFace)

    for files in L1:
      p_file = os.path.join(isFace,files)
      img = cv2.imread(p_file ,0)
      dataset.append([img,1])
    
    for files in L2:
      p_file = os.path.join(notFace,files)
      img = cv2.imread(p_file ,0)
      dataset.append([img,0]) 

    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)
    return dataset
