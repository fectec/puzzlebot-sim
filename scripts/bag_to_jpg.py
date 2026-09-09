#!/usr/bin/env python3

import os
import cv2
import argparse
import numpy as np 
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py
from cv_bridge import CvBridge

def extract_images(bag_dir, output_dir, topic_name, frame_skip):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    storage_options = rosbag2_py.StorageOptions(uri=bag_dir, storage_id='sqlite3')
    converter_options = rosbag2_py.ConverterOptions(input_serialization_format='cdr', output_serialization_format='cdr')

    reader = rosbag2_py.SequentialReader()
    try:
        reader.open(storage_options, converter_options)
    except Exception as e:
        print(f"Error opening the bag: {e}")
        return

    topic_types = reader.get_all_topics_and_types()
    type_map = {topic.name: topic.type for topic in topic_types}
    
    if topic_name not in type_map:
        print(f"Error: Topic '{topic_name}' was not found.")
        return

    msg_type = get_message(type_map[topic_name])
    bridge = CvBridge()

    storage_filter = rosbag2_py.StorageFilter(topics=[topic_name])
    reader.set_filter(storage_filter)

    count = 0
    saved_count = 0

    print(f"Extracting frames from topic {topic_name}...")
    
    while reader.has_next():
        (topic, data, t) = reader.read_next()
        
        if count % frame_skip == 0:
            msg = deserialize_message(data, msg_type)
            try:
                # CHECK IF COMPRESSED OR RAW
                if 'CompressedImage' in msg_type.__name__:
                    # Decompress JPEG bytes using OpenCV
                    np_arr = np.frombuffer(msg.data, np.uint8)
                    cv_img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                else:
                    # Convert standard ROS Image
                    cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
                
                if cv_img is not None:
                    filename = os.path.join(output_dir, f"frame_{saved_count:04d}.jpg")
                    cv2.imwrite(filename, cv_img)
                    saved_count += 1
            except Exception as e:
                print(f"Error converting frame {count}: {e}")
                
        count += 1

    print(f"Done! Successfully saved {saved_count} images in '{output_dir}'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract .jpg images from a ROS 2 Bag.')
    parser.add_argument('bag_path', type=str, help='Path to the rosbag folder')
    parser.add_argument('--output', type=str, default='dataset_frames', help='Destination folder')
    parser.add_argument('--topic', type=str, default='/image_raw', help='Camera topic to extract')
    parser.add_argument('--skip', type=int, default=5, help='Extract 1 frame every X frames')
    
    args = parser.parse_args()
    
    extract_images(args.bag_path, args.output, args.topic, args.skip)