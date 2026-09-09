# 1. Standard Python Libraries
import os

# 2. ROS 2 Core Packages
from ament_index_python.packages import get_package_share_directory

# 3. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource

# 4. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node

def get_cfg(pkg_dir, env_type, file_name):
    env_path = os.path.join(pkg_dir, 'config', env_type, file_name)
    if os.path.exists(env_path): return env_path
    return os.path.join(pkg_dir, 'config', file_name)

def generate_launch_description():
    pkg_description = get_package_share_directory('puzzlebot_description')
    pkg_control     = get_package_share_directory('puzzlebot_control')
    pkg_hardware    = get_package_share_directory('puzzlebot_hardware')
    pkg_bringup     = get_package_share_directory('puzzlebot_bringup')
    pkg_navigation  = get_package_share_directory('puzzlebot_navigation')

    env            = 'simulation'
    sim_time_dict  = {'use_sim_time': True}
    sim_time_str   = str(sim_time_dict['use_sim_time'])
    
    # ==========================================
    # LAYER 1: BASE / SIMULATION 
    # ==========================================
    simulation_gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_description, 'launch', 'simulation_gazebo.launch.py'))
    )

    # ==========================================
    # LAYER 2: CONTROLLERS & HARDWARE
    # ==========================================
    simulation_controller_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_control, 'launch', 'simulation_controller.launch.py'))
    )
    twist_mux_node = Node(
        package='twist_mux', executable='twist_mux', output='screen',
        remappings=[('/cmd_vel_out', '/cmd_vel_raw')], 
        parameters=[get_cfg(pkg_control, env, 'twist_mux.yaml'), sim_time_dict]
    )
    twist_mux_stamper_node = Node(
        package='twist_stamper', executable='twist_stamper', name='twist_mux_stamper', output='screen',
        parameters=[{'frame_id': 'base_footprint'}, sim_time_dict], 
        remappings=[('/cmd_vel_in', '/cmd_vel_raw'), ('/cmd_vel_out', '/cmd_vel_raw_stamped')]
    )
    accel_limiter_node = Node(
        package='puzzlebot_hardware', executable='accel_limiter.py', name='accel_limiter', output='screen',
        parameters=[get_cfg(pkg_hardware, env, 'accel_limiter.yaml'), sim_time_dict]
    )
    forklift_controller_node = Node(
        package='puzzlebot_control', executable='forklift_controller.py', name='forklift_controller', output='screen',
        parameters=[get_cfg(pkg_control, env, 'forklift_controller.yaml'), get_cfg(pkg_control, env, 'forklift_mux.yaml'), sim_time_dict]
    )

    controllers_layer_timer = TimerAction(
        period=10.0,
        actions=[
            simulation_controller_launch, twist_mux_node, twist_mux_stamper_node, accel_limiter_node, 
            forklift_controller_node
        ]
    )

    # ==========================================
    # LAYER 3: TELEOP
    # ==========================================
    joystick_teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_control, 'launch', 'joystick_teleop.launch.py')),
        launch_arguments={'env_type': env, 'use_sim_time': sim_time_str, 'config_file': get_cfg(pkg_control, env, 'joystick_teleop.yaml')}.items()
    )
    keyboard_teleop_node = Node(
        package='teleop_twist_keyboard', executable='teleop_twist_keyboard', name='keyboard_teleop', output='screen',
        remappings=[('/cmd_vel', '/keyboard/cmd_vel')], parameters=[sim_time_dict], prefix='xterm -e'
    )
    template_teleop_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_control, 'launch', 'template_teleop.launch.py')),
        launch_arguments={'env_type': env, 'use_sim_time': sim_time_str}.items()
    )

    teleop_layer_timer = TimerAction(
        period=12.0,
        actions=[joystick_teleop_launch, keyboard_teleop_node, template_teleop_launch]
    )

    # ==========================================
    # LAYER 4: NAVIGATION
    # ==========================================
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_navigation, 'launch', 'nav2.launch.py')),
        launch_arguments={
            'use_sim_time': sim_time_str, 'env_type': env, 
            'config_file':  get_cfg(pkg_navigation, env, 'nav2.yaml'), 
            'map_file':     os.path.join(pkg_navigation, 'maps', 'simulation_e80_factory.yaml')
        }.items()
    )
    fixed_aruco_pose_streamer_node = Node(
        package='puzzlebot_navigation', executable='fixed_aruco_pose_streamer.py', name='fixed_aruco_pose_streamer', output='screen',
        parameters=[
            get_cfg(pkg_navigation, env, 'fixed_aruco_pose_streamer.yaml'),
            {'aruco_file': get_cfg(pkg_navigation, env, 'fixed_arucos_poses.json')},
            sim_time_dict
        ]
    )
    
    navigation_layer_timer = TimerAction(
        period=14.0,
        actions=[nav2_launch, fixed_aruco_pose_streamer_node]
    )

    # ==========================================
    # LAYER 5: VISUALIZATION
    # ==========================================
    rviz_node = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        arguments=['-d', os.path.join(pkg_description, 'rviz_config', 'simulation_puzzlebot.rviz')],
        parameters=[sim_time_dict]
    )
    foxglove_bridge_node = Node(
        package='foxglove_bridge', executable='foxglove_bridge', name='foxglove_bridge', output='screen',
        parameters=[get_cfg(pkg_bringup, env, 'foxglove_bridge.yaml'), sim_time_dict]
    )
    
    visualization_layer_timer = TimerAction(
        period=16.0,
        actions=[rviz_node, foxglove_bridge_node]
    )

    return LaunchDescription([
        simulation_gazebo_launch,
        controllers_layer_timer,
        teleop_layer_timer,
        navigation_layer_timer,     
        visualization_layer_timer
    ])