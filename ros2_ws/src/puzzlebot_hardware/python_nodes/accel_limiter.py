#!/usr/bin/env python3

# 1. Standard Python Libraries
import sys

# 2. ROS 2 Core, Parameters & Services
import rclpy
from rcl_interfaces.msg import SetParametersResult
from rclpy.node import Node
from rclpy.parameter import Parameter
from std_srvs.srv import SetBool

# 3. ROS 2 Standard & Sensor Messages
from geometry_msgs.msg import Twist, TwistStamped
from std_msgs.msg import String

# 4. TF2, Transformations & Image Bridge

# 5. ROS 2 QoS Profiles
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy

CONTROL_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)

STATE_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1
)

class AccelLimiterNode(Node):
    """
    Acts as a safety and smoothing filter between velocity command sources
    and the robot hardware.

    It subscribes to raw velocity commands and applies a slew-rate limit based on maximum 
    allowed linear and angular accelerations. This prevents sudden jerks, protects the motors 
    from high current spikes, and ensures smooth physical motion by stepping the current 
    velocity toward the target velocity over time.
    """
    def __init__(self):
        super().__init__('accel_limiter')
        
        # Declare parameters
        self.declare_parameter('update_rate', 60.0)         # Hz
        self.declare_parameter('max_linear_accel', 0.3)     # m/s^2
        self.declare_parameter('max_angular_accel', 1.0)    # rad/s^2
        self.declare_parameter('input_timeout', 0.2)        # s

        # Load parameters
        self.max_v_accel = self.get_parameter('max_linear_accel').value
        self.max_w_accel = self.get_parameter('max_angular_accel').value
        self.input_timeout = self.get_parameter('input_timeout').value
        self.update_rate = self.get_parameter('update_rate').value

        self.dt = 1.0 / float(self.update_rate)

        # Register the on-set-parameters callback for dynamic parameter updates
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Immediately validate the initial values
        init_params = [
            Parameter('max_linear_accel', Parameter.Type.DOUBLE, float(self.max_v_accel)),
            Parameter('max_angular_accel', Parameter.Type.DOUBLE, float(self.max_w_accel)),
            Parameter('update_rate', Parameter.Type.DOUBLE, float(self.update_rate)),
            Parameter('input_timeout', Parameter.Type.DOUBLE, float(self.input_timeout)),
        ]
        result = self.parameter_callback(init_params)
        if not result.successful:
            raise RuntimeError(f"Parameter validation failed: {result.reason}")

        # Initialize state variables
        self.target_v, self.target_w = 0.0, 0.0
        self.current_v, self.current_w = 0.0, 0.0
        self.last_msg_time = self.get_clock().now()

        # Publishers & Subscribers        
        self.pub = self.create_publisher(
            Twist, 
            '/cmd_vel', 
            CONTROL_QOS
        )

        self.create_subscription(
            TwistStamped, 
            '/cmd_vel_raw_stamped', 
            self.callback, 
            CONTROL_QOS 
        )

        # Task Server
        self.is_enabled = True
        self.state = "RUNNING"
        self.enable_srv = self.create_service(SetBool, '~/enable', self.enable_callback)
        self.status_pub = self.create_publisher(String, '~/status', STATE_QOS)
        self.status_timer = self.create_timer(0.1, self.publish_status)

        self.timer = self.create_timer(self.dt, self.timer_callback)
        
        self.get_logger().info("AccelLimiter Start.")

    def publish_status(self):
        self.status_pub.publish(String(data=self.state))

    def enable_callback(self, request, response):
        self.is_enabled = request.data
        self.state = "RUNNING" if self.is_enabled else "IDLE"
        
        response.success = True
        response.message = f"Accel Limiter {'Enabled' if self.is_enabled else 'Disabled'}"
        self.get_logger().info(response.message)
        return response

    def callback(self, msg: TwistStamped):
        if not self.is_enabled:
            return
            
        self.target_v = msg.twist.linear.x
        self.target_w = msg.twist.angular.z
        self.last_msg_time = self.get_clock().now()

    def timer_callback(self):
        now = self.get_clock().now()
        elapsed = (now - self.last_msg_time).nanoseconds / 1e9

        # If the upstream nodes go silent, force target to zero
        if elapsed > self.input_timeout:
            if self.target_v != 0.0 or self.target_w != 0.0:
                self.get_logger().warn("Input timeout! Forcing ramp down to zero.", throttle_duration_sec=2.0)
            self.target_v, self.target_w = 0.0, 0.0
            
        if not self.is_enabled:
            self.target_v, self.target_w = 0.0, 0.0

        # Linear smoothing 
        v_step = self.max_v_accel * self.dt
        dv = self.target_v - self.current_v
        self.current_v += max(-v_step, min(dv, v_step))

        # Angular smoothing 
        w_step = self.max_w_accel * self.dt
        dw = self.target_w - self.current_w
        self.current_w += max(-w_step, min(dw, w_step))

        out = Twist()
        out.linear.x, out.angular.z = self.current_v, self.current_w
        self.pub.publish(out)

    def parameter_callback(self, params: list[Parameter]) -> SetParametersResult:
        for param in params:
            if param.name == 'max_linear_accel':
                if not isinstance(param.value, (int, float)) or param.value <= 0.0:
                    return SetParametersResult(successful=False, reason="Must be > 0.0")
                self.max_v_accel = float(param.value)
                self.get_logger().info(f"Updated max_linear_accel to: {self.max_v_accel}")
                
            elif param.name == 'max_angular_accel':
                if not isinstance(param.value, (int, float)) or param.value <= 0.0:
                    return SetParametersResult(successful=False, reason="Must be > 0.0")
                self.max_w_accel = float(param.value)
                self.get_logger().info(f"Updated max_angular_accel to: {self.max_w_accel}")

            elif param.name == 'input_timeout':
                if not isinstance(param.value, (int, float)) or param.value <= 0.0:
                    return SetParametersResult(successful=False, reason="Must be > 0.0")
                self.input_timeout = float(param.value)
                self.get_logger().info(f"Updated input_timeout to: {self.input_timeout}")
                
            elif param.name == 'update_rate':
                if not isinstance(param.value, (int, float)) or param.value <= 0.0:
                    return SetParametersResult(successful=False, reason="update_rate (Hz) must be > 0")
                
                self.dt = 1.0 / float(param.value)
                
                if hasattr(self, 'timer'):
                    self.timer.cancel()
                    self.timer = self.create_timer(self.dt, self.timer_callback)
                
                self.get_logger().info(f"Updated update_rate to: {param.value} Hz (dt={self.dt:.4f}s)")

        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)

    try:
        node = AccelLimiterNode()
    except Exception as e:
        print(f"[FATAL] AccelLimiter failed to initialize: {e}", file=sys.stderr)
        rclpy.shutdown()
        return

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down AccelLimiter...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()