import math
import json

from numpy import array

#A point has a reference frame/s in which it is defined.
# A Frame is defined either as a "world frame" or in reference to another frame
# When is is referenced by another frame it is reference by a matrix
# The Matrix has 3 vectors for the location of the referenced frame origin and one for orientation
# 
# cos -sin
# sin  cos  

class Frame:
    
    def __init__(self, parent_frame, rotation_matrix: array, translation_vector: array):
        self.parent_frame = parent_frame
        self.rotation_matrix = rotation_matrix
        self.translation_vector = translation_vector
        self.child_frames = []
        if parent_frame is not None:
            parent_frame.add_child_frame(self)

    def add_child_frame(self, child_frame):
        self.child_frames.append(child_frame)

class Point:
    def __init__(self, reference_frame: Frame, location):
        self.reference_frame = reference_frame
        self.location = location