# 1. Standard Python Libraries
from pathlib import Path
import os

# 2. ROS 2 Core Packages
from ament_index_python.packages import get_package_share_directory

# 3. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration

# 4. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_description = get_package_share_directory('puzzlebot_description')
    pkg_ros_gz_sim  = get_package_share_directory('ros_gz_sim')

    model_file   = LaunchConfiguration('model_file')
    world_file   = LaunchConfiguration('world_file')
    config_file  = LaunchConfiguration('config_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    model_file_arg = DeclareLaunchArgument(
        'model_file',
        default_value=os.path.join(pkg_description, 'urdf', 'puzzlebot.urdf.xacro'),
        description='Absolute path to robot URDF file'
    )
    world_file_arg = DeclareLaunchArgument(
        'world_file',
        default_value=os.path.join(pkg_description, 'worlds', 'e80_factory.sdf'),
        description='Absolute path to the Gazebo SDF world file'
    )
    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(pkg_description, 'gazebo_config', 'simulation_gazebo.config'),
        description='Absolute path to the Gazebo GUI config file'
    )
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',                          
        description='Use simulation (Gazebo) clock or real wall time'
    )

    robot_description = ParameterValue(
        Command(['xacro ', model_file, ' is_ignition:=true']),
        value_type=str
    )

    ign_resource_path = SetEnvironmentVariable(
        'IGN_GAZEBO_RESOURCE_PATH',
        str(Path(pkg_description).parent.resolve())
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')]),
        launch_arguments=[
            ('gz_args', [' -v 4', ' -r ', world_file, ' --gui-config ', config_file])
        ]
    )

    gz_spawn_entity_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'puzzlebot',
            '-x', '-1.8',
            '-y', '0.0',
            '-z', '0.0',
            '-Y', '-1.57'
        ],
        output='screen'
    )

    ros_gz_parameter_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
            '/scan@sensor_msgs/msg/LaserScan[ignition.msgs.LaserScan',
            '/camera_info@sensor_msgs/msg/CameraInfo[ignition.msgs.CameraInfo'
        ],
        output='screen'
    )

    ros_gz_image_bridge_node = Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=['/image_raw', '/debug/image_raw'],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    return LaunchDescription([
        model_file_arg,
        world_file_arg,
        config_file_arg,
        use_sim_time_arg,
        ign_resource_path,
        robot_state_publisher_node,
        gazebo_launch,
        gz_spawn_entity_node,
        ros_gz_parameter_bridge_node,
        ros_gz_image_bridge_node
    ])