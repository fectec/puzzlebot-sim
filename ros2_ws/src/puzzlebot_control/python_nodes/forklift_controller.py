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
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState, Joy
from std_msgs.msg import (
    Bool,
    Float32,
    Float64,
    Float64MultiArray,
    String
)

# 4. ROS 2 QoS Profiles
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy
from rclpy.qos import qos_profile_sensor_data

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

class ForkliftControllerNode(Node):
    """
    Controls the forklift mechanism to adjust the forks height.
    Receives target heights and converts them to motor commands based on limits.
    """
    def __init__(self):
        super().__init__('forklift_controller', automatically_declare_parameters_from_overrides=True, allow_undeclared_parameters=True)

        # Declare parameters
        if not self.has_parameter('update_rate'):
            self.declare_parameter('update_rate', 15.0)
        if not self.has_parameter('max_z'):
            self.declare_parameter('max_z', 0.23825)
        if not self.has_parameter('step_size'):
            self.declare_parameter('step_size', 0.003)
        if not self.has_parameter('forks_joystick_axis'):
            self.declare_parameter('forks_joystick_axis', 7)
        if not self.has_parameter('kp'):
            self.declare_parameter('kp', 5.0)
        if not self.has_parameter('joy_activate_threshold'):
            self.declare_parameter('joy_activate_threshold', 0.5)
        if not self.has_parameter('max_sim_velocity'):
            self.declare_parameter('max_sim_velocity', 0.06)
        if not self.has_parameter('target_tolerance'):
            self.declare_parameter('target_tolerance', 0.005)

        # Load parameters
        self.update_rate = self.get_parameter('update_rate').value
        self.max_z = self.get_parameter('max_z').value
        self.step_size = self.get_parameter('step_size').value
        self.forks_joystick_axis = self.get_parameter('forks_joystick_axis').value
        self.kp = self.get_parameter('kp').value
        self.joy_activate_threshold = self.get_parameter('joy_activate_threshold').value
        self.max_sim_velocity = self.get_parameter('max_sim_velocity').value
        self.target_tolerance = self.get_parameter('target_tolerance').value

        # Register the on-set-parameters callback for dynamic parameter updates
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Immediately validate the initial values
        init_params = [
            Parameter('update_rate', Parameter.Type.DOUBLE, float(self.update_rate)),
            Parameter('max_z', Parameter.Type.DOUBLE, float(self.max_z)),
            Parameter('step_size', Parameter.Type.DOUBLE, float(self.step_size)),
            Parameter('forks_joystick_axis', Parameter.Type.INTEGER, int(self.forks_joystick_axis)),
            Parameter('kp', Parameter.Type.DOUBLE, float(self.kp)),
            Parameter('joy_activate_threshold', Parameter.Type.DOUBLE, float(self.joy_activate_threshold)),
            Parameter('max_sim_velocity', Parameter.Type.DOUBLE, float(self.max_sim_velocity)),
            Parameter('target_tolerance', Parameter.Type.DOUBLE, float(self.target_tolerance))
        ]
        result = self.parameter_callback(init_params)
        if not result.successful:
            raise RuntimeError(f"Parameter validation failed: {result.reason}")

        # Setup Mux Architecture
        self.sources = {}
        self.locks = {}
        self._setup_mux()

        # Publishers
        self.sim_forks_cmd_pub = self.create_publisher(Float64MultiArray, '/forks_controller/commands', CONTROL_QOS)
        
        # Feedback Subscribers
        self.sim_forks_joint_states_sub = self.create_subscription(JointState, '/joint_states', self.sim_joint_state_callback, qos_profile_sensor_data)

        # State Variables
        self.active_target_norm = 0.0       
        self.current_feedback_norm = 0.0    

        # Task Server
        self.is_enabled = True
        self.state = "IDLE"
        self.enable_srv = self.create_service(SetBool, '~/enable', self.enable_callback)
        self.status_pub = self.create_publisher(String, '~/status', STATE_QOS)
        self.status_timer = self.create_timer(0.1, self.publish_status)

        self.timer = self.create_timer(1.0 / self.update_rate, self.control_loop)
        self.get_logger().info("ForkliftController Start.")

    def _setup_mux(self):
        """Dynamically parses locks and topics from yaml to build the mux."""
        # Parse Locks
        locks_params = self.get_parameters_by_prefix('locks')
        lock_names = set(k.split('.')[0] for k in locks_params.keys())
        for lck in lock_names:
            topic_str = locks_params.get(f"{lck}.topic").value
            timeout_val = locks_params.get(f"{lck}.timeout").value
            priority_val = locks_params.get(f"{lck}.priority").value
            
            sub = self.create_subscription(Bool, topic_str, lambda msg, n=lck: self.lock_cb(msg, n), CONTROL_QOS)
            
            self.locks[lck] = {
                'topic': topic_str, 'timeout': float(timeout_val), 'priority': int(priority_val),
                'sub': sub, 'last_time': self.get_clock().now(), 'active': False
            }
            self.get_logger().info(f"[MUX] Registered Lock: {lck} -> {topic_str} (Priority: {priority_val})")

        # Parse Sources
        topics_params = self.get_parameters_by_prefix('topics')
        source_names = set(k.split('.')[0] for k in topics_params.keys())

        for src in source_names:
            topic_param = topics_params.get(f"{src}.topic")
            timeout_param = topics_params.get(f"{src}.timeout")
            priority_param = topics_params.get(f"{src}.priority")
            
            topic_str = topic_param.value if topic_param else ""
            priority_val = priority_param.value if priority_param else 0
            
            src_lower = src.lower()
            topic_lower = topic_str.lower()
            
            is_joy = ('joy' in src_lower or 'joy' in topic_lower)
            is_twist = ('twist' in src_lower)
            is_joy_or_twist = is_joy or is_twist

            timeout_val = float(timeout_param.value) if (timeout_param and is_joy_or_twist) else 0.0

            if is_joy:
                sub = self.create_subscription(Joy, topic_str, lambda msg, n=src: self.joy_mux_cb(msg, n), qos_profile_sensor_data)
            elif is_twist:
                sub = self.create_subscription(Twist, topic_str, lambda msg, n=src: self.twist_mux_cb(msg, n), CONTROL_QOS)
            else:
                sub = self.create_subscription(Float64, topic_str, lambda msg, n=src: self.float_mux_cb(msg, n), CONTROL_QOS)
                
            self.sources[src] = {
                'name': src, 'topic': topic_str, 'timeout': timeout_val, 'priority': int(priority_val),
                'sub': sub, 'last_time': self.get_clock().now(), 'value': 0.0, 'active': False,
                'is_joy': is_joy_or_twist
            }
            self.get_logger().info(f"[MUX] Registered Source: {src} -> {topic_str} (Priority: {priority_val})")

    def publish_status(self):
        self.status_pub.publish(String(data=self.state))

    def lock_cb(self, msg, name):
        self.locks[name]['active'] = msg.data
        self.locks[name]['last_time'] = self.get_clock().now()

    def joy_mux_cb(self, msg, name):
        if self.forks_joystick_axis < len(msg.axes):
            self.sources[name]['value'] = msg.axes[self.forks_joystick_axis]
            self.sources[name]['active'] = True
            self.sources[name]['last_time'] = self.get_clock().now()

    def twist_mux_cb(self, msg, name):
        self.sources[name]['value'] = msg.linear.z
        self.sources[name]['active'] = True
        self.sources[name]['last_time'] = self.get_clock().now()

    def float_mux_cb(self, msg, name):
        self.sources[name]['value'] = max(0.0, min(1.0, msg.data))
        self.sources[name]['active'] = True
        self.sources[name]['last_time'] = self.get_clock().now()

    def enable_callback(self, request, response):
        self.is_enabled = request.data
        if not self.is_enabled:
            self.state = "DISABLED"
        response.success = True
        return response

    def sim_joint_state_callback(self, msg):
        if not msg.velocity: return
        if 'forks_joint' in msg.name:
            idx = msg.name.index('forks_joint')
            self.current_feedback_norm = max(0.0, min(1.0, msg.position[idx] / self.max_z))

    def control_loop(self):
        if not self.is_enabled:
            self.halt_robot()
            return

        now = self.get_clock().now()

        # Evaluate Locks
        is_locked = False
        for name, lck in self.locks.items():
            dt = (now - lck['last_time']).nanoseconds / 1e9
            if lck['active'] and (lck['timeout'] == 0.0 or dt <= lck['timeout']):
                is_locked = True
                break

        if is_locked:
            self.state = "LOCKED"
            self.halt_robot()
            return

        # Evaluate Mux Priority Tree
        highest_priority = -1
        active_source = None

        for name, src in self.sources.items():
            dt = (now - src['last_time']).nanoseconds / 1e9
            is_timed_out = src['timeout'] > 0.0 and dt > src['timeout']
            
            if is_timed_out:
                src['active'] = False

            if src['active'] and src['priority'] > highest_priority:
                if src['is_joy']:
                    # Joystick must be physically deflected to claim priority
                    if abs(src['value']) > self.joy_activate_threshold:
                        highest_priority = src['priority']
                        active_source = src
                else:
                    highest_priority = src['priority']
                    active_source = src

        target_reached = False
        # Extract Value and Sync Overridden Sources
        if active_source:
            if active_source['is_joy']:
                if active_source['value'] > self.joy_activate_threshold:
                    self.active_target_norm += self.step_size
                elif active_source['value'] < -self.joy_activate_threshold:
                    self.active_target_norm -= self.step_size
            else:
                target = active_source['value']
                if target > self.active_target_norm + self.step_size:
                    self.active_target_norm += self.step_size
                elif target < self.active_target_norm - self.step_size:
                    self.active_target_norm -= self.step_size
                else:
                    self.active_target_norm = target
                    target_reached = True

        self.active_target_norm = max(0.0, min(1.0, self.active_target_norm))

        # Output to Simulation Only
        error_norm = self.active_target_norm - self.current_feedback_norm
        error_metric = error_norm * self.max_z
        velocity_cmd = max(-self.max_sim_velocity, min(self.max_sim_velocity, self.kp * error_metric))

        if abs(error_norm) < self.target_tolerance:
            velocity_cmd = 0.0

        # State Machine Logic
        if active_source:
            if active_source['is_joy']:
                self.state = f"RUNNING_{active_source['name'].upper()}"
            else:
                is_tracking_done = target_reached and (abs(error_norm) < self.target_tolerance)
                if not is_tracking_done:
                    self.state = f"RUNNING_{active_source['name'].upper()}"
                else:
                    if self.state != "REACHED":
                        self.state = "REACHED"
                        self.reached_time = now
                    else:
                        if not hasattr(self, 'reached_time'):
                            self.reached_time = now
                        if (now - self.reached_time).nanoseconds / 1e9 > 1.0:
                            self.state = "IDLE"
                            active_source['active'] = False
        else:
            self.state = "IDLE"

        self.sim_forks_cmd_pub.publish(Float64MultiArray(data=[float(velocity_cmd)]))

    def halt_robot(self):
        self.sim_forks_cmd_pub.publish(Float64MultiArray(data=[0.0]))

    def parameter_callback(self, params):
        """Validates and applies updated node parameters strictly."""
        new = {p.name: p.value for p in params}

        if 'update_rate' in new:
            ur = float(new['update_rate'])
            if ur <= 0.0:
                return SetParametersResult(successful=False, reason="update_rate must be > 0.")
            self.update_rate = ur
            if hasattr(self, 'timer'):
                self.timer.cancel()
                self.timer = self.create_timer(1.0 / self.update_rate, self.control_loop)
            self.get_logger().info(f"Dynamically updated update_rate to: {self.update_rate} Hz.")

        if 'max_z' in new:
            mz = float(new['max_z'])
            if mz <= 0.0:
                return SetParametersResult(successful=False, reason="max_z must be > 0.")
            self.max_z = mz
            self.get_logger().info(f"Dynamically updated max_z to: {self.max_z} m.")

        if 'step_size' in new:
            ss = float(new['step_size'])
            if ss <= 0.0:
                return SetParametersResult(successful=False, reason="step_size must be > 0.")
            self.step_size = ss
            self.get_logger().info(f"Dynamically updated step_size to: {self.step_size}.")

        if 'forks_joystick_axis' in new:
            fj = int(new['forks_joystick_axis'])
            if fj < 0:
                return SetParametersResult(successful=False, reason="forks_joystick_axis must be >= 0.")
            self.forks_joystick_axis = fj
            self.get_logger().info(f"Dynamically updated forks_joystick_axis to: {self.forks_joystick_axis}.")

        if 'kp' in new:
            kp = float(new['kp'])
            if kp <= 0.0:
                return SetParametersResult(successful=False, reason="kp must be > 0.")
            self.kp = kp
            self.get_logger().info(f"Dynamically updated kp to: {self.kp}.")

        if 'joy_activate_threshold' in new:
            jt = float(new['joy_activate_threshold'])
            if jt < 0.0 or jt > 1.0:
                return SetParametersResult(
                    successful=False,
                    reason="joy_activate_threshold must be between 0.0 and 1.0."
                )
            self.joy_activate_threshold = jt
            self.get_logger().info(
                f"Dynamically updated joy_activate_threshold to: {self.joy_activate_threshold}."
            )

        if 'max_sim_velocity' in new:
            mv = float(new['max_sim_velocity'])
            if mv <= 0.0:
                return SetParametersResult(successful=False, reason="max_sim_velocity must be > 0.")
            self.max_sim_velocity = mv
            self.get_logger().info(
                f"Dynamically updated max_sim_velocity to: {self.max_sim_velocity} m/s."
            )

        if 'target_tolerance' in new:
            tt = float(new['target_tolerance'])
            if tt < 0.0:
                return SetParametersResult(successful=False, reason="target_tolerance must be >= 0.")
            self.target_tolerance = tt
            self.get_logger().info(
                f"Dynamically updated target_tolerance to: {self.target_tolerance}."
            )

        return SetParametersResult(successful=True)
    
def main(args=None):
    rclpy.init(args=args)

    try:
        node = ForkliftControllerNode()
    except Exception as e:
        print(f"[FATAL] ForkliftControllerNode failed to initialize: {e}", file=sys.stderr)
        rclpy.shutdown()
        return

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down ForkliftControllerNode...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()