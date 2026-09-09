#!/usr/bin/env python3

# 1. Standard Python Libraries
import json
import os
import sys

# 2. ROS 2 Core, Parameters & Services
import rclpy
from ament_index_python.packages import get_package_share_directory
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_srvs.srv import SetBool

# 3. ROS 2 Standard & Sensor Messages
from geometry_msgs.msg import TransformStamped
from std_msgs.msg import String

# 4. TF2, Transformations & Image Bridge
from tf2_ros import StaticTransformBroadcaster

# Fix for transforms3d numpy float deprecation
import numpy as np
if not hasattr(np, 'float'):
    np.float = float

from tf_transformations import quaternion_from_euler

# 5. ROS 2 QoS Profiles
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

STATE_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)

class FixedArucoPoseStreamerNode(Node):
    """
    Reads a list of known ArUco marker poses from a JSON file and streams them
    as Static Transforms (map -> aruco_X) to the ROS 2 TF tree.
    """
    def __init__(self):
        super().__init__('fixed_aruco_pose_streamer')
        
        # Declare parameters
        self.declare_parameter('update_rate', 1.0)                          # Hz
        self.declare_parameter('aruco_file', 'fixed_arucos_poses.json')     # string  

        # Load parameters
        self.update_rate = self.get_parameter('update_rate').value
        self.aruco_file = self.get_parameter('aruco_file').value

        # Register the on-set-parameters callback for dynamic parameter updates
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Immediately validate the initial values
        init_params = [
            Parameter('update_rate', Parameter.Type.DOUBLE, float(self.update_rate)),
            Parameter('aruco_file', Parameter.Type.STRING, str(self.aruco_file)),
        ]
        result = self.parameter_callback(init_params)
        if not result.successful:
            raise RuntimeError(f"Parameter validation failed: {result.reason}")

        # TF Broadcaster
        self.static_tf_broadcaster = StaticTransformBroadcaster(self)

        # Task Server
        self.is_enabled = True
        self.state = "RUNNING"
        self.enable_srv = self.create_service(SetBool, '~/enable', self.enable_callback)
        self.status_pub = self.create_publisher(String, '~/status', STATE_QOS)
        self.status_timer = self.create_timer(0.1, self.publish_status)

        # Broadcast transforms once at startup
        self.broadcast_static_transforms()

        self.get_logger().info("FixedArucoPoseStreamer Start.")

    def publish_status(self):
        self.status_pub.publish(String(data=self.state))

    def enable_callback(self, request, response):
        self.is_enabled = request.data
        self.state = "RUNNING" if self.is_enabled else "IDLE"
        
        if self.is_enabled:
            # Re-broadcast just in case it was disabled and needs a refresh
            self.broadcast_static_transforms()

        response.success = True
        response.message = f"FixedArucoPoseStreamer {'Enabled' if self.is_enabled else 'Disabled'}"
        self.get_logger().info(response.message)
        return response

    def broadcast_static_transforms(self):
        """Reads the JSON file and publishes the static transforms for all markers."""
        try:
            pkg_dir = get_package_share_directory('puzzlebot_navigation')
            file_path = os.path.join(pkg_dir, 'config', self.aruco_file)
            
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            transforms = []
            for aruco in data.get("arucos", []):
                t = TransformStamped()
                t.header.stamp = self.get_clock().now().to_msg()
                t.header.frame_id = 'map'
                t.child_frame_id = f"aruco_{aruco['id']}_fixed"

                # Translation
                t.transform.translation.x = float(aruco['x'])
                t.transform.translation.y = float(aruco['y'])
                t.transform.translation.z = float(aruco['z'])

                # Rotation (Euler to Quaternion)
                q = quaternion_from_euler(
                    float(aruco['roll']),
                    float(aruco['pitch']),
                    float(aruco['yaw'])
                )
                t.transform.rotation.x = q[0]
                t.transform.rotation.y = q[1]
                t.transform.rotation.z = q[2]
                t.transform.rotation.w = q[3]

                transforms.append(t)
            
            # Send all static transforms at once
            self.static_tf_broadcaster.sendTransform(transforms)
            self.get_logger().info(f"Successfully broadcasted {len(transforms)} static ArUco poses.")

        except Exception as e:
            self.get_logger().error(f"Failed to load or broadcast ArUco poses from {self.aruco_file}: {e}")

    def parameter_callback(self, params):
        """Validates and applies updated node parameters."""
        for param in params:
            if param.name == 'update_rate':
                if not isinstance(param.value, (int, float)) or param.value <= 0.0:
                    return SetParametersResult(successful=False, reason="update_rate must be > 0.")
                self.update_rate = float(param.value)

                if hasattr(self, 'timer'):
                    self.timer.cancel()
                    self.timer = self.create_timer(1.0 / self.update_rate, self.spin_task)

                self.get_logger().info(f"Dynamically updated update_rate to: {self.update_rate} Hz.")

            elif param.name == 'aruco_file':
                if not isinstance(param.value, str) or not param.value:
                    return SetParametersResult(successful=False, reason="aruco_file must be a valid string.")
                self.aruco_file = str(param.value)
                
                # Re-broadcast with the new file
                if hasattr(self, 'static_tf_broadcaster'):
                    self.broadcast_static_transforms()
                    
                self.get_logger().info(f"Dynamically updated aruco_file to: {self.aruco_file}.")

        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)

    try:
        node = FixedArucoPoseStreamerNode()
    except Exception as e:
        print(f"[FATAL] FixedArucoPoseStreamer failed to initialize: {e}", file=sys.stderr)
        rclpy.shutdown()
        return

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down FixedArucoPoseStreamer...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()