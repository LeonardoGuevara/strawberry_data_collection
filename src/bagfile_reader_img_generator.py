from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore
from rosbags.image import message_to_cvimage
import cv2
import numpy as np
import os
import re

bagdata_path='C:/Users/gueva/OneDrive/Documentos/Leo/Rosbags' # main directory path
image_path='C:/Users/gueva/OneDrive/Documentos/Leo/Rosbags/Images' # directory path for storing images
tables = [1,2,3,4,5,6,7,8,9,10]
#tables = [8,9] # for testing only
#FOR LOOP FOR TABLES
for table in tables:
    date_old="none" # initial value
    #table=9 # for testing only
    #FOR LOOP FOR BAG FILE FOLDERS
    files = os.listdir(bagdata_path+"/"+str(table))
    for bagfolder_name in files:
        #bagfolder_name='rosbag2_2024_07_02-16_12_45' # for testing only
        file_date = re.search('(\d{4}_\d{2}_\d{2})', bagfolder_name)
        date=file_date[0]
        if date_old==date:
            side="r" # second bagfile with the same date corresponds to the right side of the table
        else:
            side="l"
        date_old=date
        bagpath = Path(bagdata_path+"/"+str(table)+"/"+bagfolder_name+"/")
        imgpath = Path(image_path+"/"+str(table)+"/"+side+"/")
        print(table,bagfolder_name,side)        
        # Create a type store to use if the bag has no message definitions.
        typestore = get_typestore(Stores.ROS2_HUMBLE)

        # Create reader instance and open for reading.
        with AnyReader([bagpath], default_typestore=typestore) as reader:
            connections = [x for x in reader.connections if x.topic == '/zed/zed_node/rgb_raw/image_raw_color']
            count=0
            for connection, timestamp, rawdata in reader.messages(connections=connections):
                count=count+1
                msg = reader.deserialize(rawdata, connection.msgtype)
                img = message_to_cvimage(msg, 'bgr8')
                cv2.imshow('',img)
                cv2.waitKey(5)
                img_name = str(table)+"_"+side+"_"+date+"_"+str(count)+"_"+"rgb"+".png" 
                cv2.imwrite(os.path.join(imgpath , img_name), img)
                
            cv2.destroyAllWindows()
            
            connections = [x for x in reader.connections if x.topic == '/zed/zed_node/depth/depth_registered']
            count=0
            for connection, timestamp, rawdata in reader.messages(connections=connections):
                count=count+1
                msg = reader.deserialize(rawdata, connection.msgtype)
                img = message_to_cvimage(msg,"32FC1")
                cv2.imshow('',img)
                cv2.waitKey(5)
                img = np.array(img, dtype=np.float32)*255
                img_name = str(table)+"_"+side+"_"+date+"_"+str(count)+"_"+"depth"+".png" 
                cv2.imwrite(os.path.join(imgpath , img_name), img)

            cv2.destroyAllWindows()
