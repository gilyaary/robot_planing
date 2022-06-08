import numpy as np
THETA_INC = 36
FRAME_SYNC = 250 

#STREAM PARSER
class FrameStreamParser:

    #The call back return a numpy array:
    # [
    #     [intensity, intensity, range, range, reserved, reserved],
    #     [intensity, intensity, range, range, reserved, reserved],
    #     [intensity, intensity, range, range, reserved, reserved],
    # ]
    # Each row is a different angle in the current frame set

    def __init__(self, callback):
        pass
        self.current_measurement_set = np.zeros((360,2)) #360 measurements of intensity, distance
        self.current_frame_index = 59
        self.current_frame_data_index = -1
        self.first_sync_found = False
        self.rpm = None
        self.callback = callback
        self.angle_index = 0
        self.current_measurements = np.zeros(4)
    
    def add(self, value):
        pass
        if not self.first_sync_found:
            if value != FRAME_SYNC:
                return
            else:
                self.first_sync_found = True
        
        if value == FRAME_SYNC:
            if self.current_frame_index == 59:
                self.current_measurement_set = np.zeros((360,2)) #360 measurements of intensity, distance
                self.current_frame_index = 0
                self.current_frame_data_index = 0
            else:
                self.current_frame_data_index = 0
                self.current_frame_index += 1
            #print(self.current_frame_index)
            return
        
        self.current_frame_data_index += 1
        #print ('-----', self.current_frame_data_index)intensity
        
        if self.current_frame_data_index == 1:
            #self.current_frame_data_index = value
            #print(value)
            self.angle_index = value
            self.current_measurements = np.zeros(4)
            pass
        elif self.current_frame_data_index == 2:
            pass #RPM
            self.rpm = (value, 0)
        elif self.current_frame_data_index == 3:
            pass #RPM 
            self.rpm = (self.rpm[0], value)
        elif self.current_frame_data_index == 40:
            pass #Checksum
        elif  self.current_frame_data_index == 41:
            pass #Checksum
            if self.current_frame_index == 59:
                #notify about new measurement set
                #print ('callback')
                #print(self.current_measurement_set)
                if self.callback:
                    self.callback(self.rpm, self.current_measurement_set)

        #Handle Measurement. 6 measurements per frame
        else:
            
            start_theta = self.angle_index * 6 #  36 * self.current_frame_index
            measurement_index_in_frame = int ((self.current_frame_data_index - 4) / 6)
            
            theta = (start_theta + measurement_index_in_frame)%360
            
            frame_set_measurement_index = self.current_frame_index * 6 + measurement_index_in_frame
            
            #60 measurements in frameset
            measurement_item_index =  (self.current_frame_data_index-4) % 6
            #print ('---------------- measurement_item_index:', measurement_item_index)
            
            
            
            '''
            This BUGGG was casuing many frames to return empty values !!!!
            if frame_set_measurement_index >= 60:
                #error in data
                return
            '''
            
            if measurement_item_index == 0:
                self.current_measurements[0] = value
            elif measurement_item_index == 1:
                self.current_measurements[1] = value
            elif measurement_item_index == 2:
                self.current_measurements[2] = value
            elif measurement_item_index == 3:
                self.current_measurements[3] = value
            elif measurement_item_index == 4:
                intensity = self.current_measurements[0] + self.current_measurements[1] * 256
                range = self.current_measurements[2] + self.current_measurements[3] * 256
                self.current_measurement_set[theta, 0] = intensity
                self.current_measurement_set[theta, 1] = range 
            elif measurement_item_index == 5:
                pass
            

'''

#TEST DATA
def create_frame(frame_index):
    frame = [] 
    #HEADER
    frame.append(250) #sync
    frame.append(frame_index)
    frame.append(0)#RPM
    frame.append(1)#RPM
    #Body : 6 angle measurements
    for measurement_index in range(6):
        frame.append(10)#INTEnSITY
        frame.append(10)#INTEnSITY
        frame.append(frame_index*10)#RANGE
        frame.append(2)#RANGE
        frame.append(0)#RES
        frame.append(0)#RES
    #TAIL
    frame.append(0)#CHECKSUM
    frame.append(0)#CHECKSUM

    return frame

def create_frame_set():
    frame_set = []
    for frame_index in range(10):
        frame = create_frame(frame_index)
        frame_set.append(frame)
    return frame_set

frame_sets = []
for i in range (2):
    frame_set = create_frame_set()
    frame_sets.append(frame_set)




def parser_callback (rpm, current_measurement_set):
    pass
    #print(current_measurement_set)
    for m in current_measurement_set:
        print(m)
        pass



parser = FrameStreamParser(parser_callback)
parser.add(111) #junk data before first sync
parser.add(222) #junk data before first sync
parser.add(333) #junk data before first sync
#data = []
for fs in frame_sets:
    for frame in fs:
            for value in frame:
                #data.append(value)
                parser.add(value)
'''
