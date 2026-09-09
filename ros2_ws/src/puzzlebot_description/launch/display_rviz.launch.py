# 1. Standard Python Libraries
import os

# 2. ROS 2 Core Packages
from ament_index_python.packages import get_package_share_directory

# 3. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration

# 4. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_description = get_package_share_directory('puzzlebot_description')

    model_file   = LaunchConfiguration('model_file')
    config_file  = LaunchConfiguration('config_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    model_file_arg = DeclareLaunchArgument(
        'model_file',
        default_value=os.path.join(pkg_description, 'urdf', 'puzzlebot.urdf.xacro'),
        description='Absolute path to robot URDF file'
    )

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=os.path.join(pkg_description, 'rviz_config', 'display.rviz'),
        description='Absolute path to RViz config file'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='False',
        description='Use simulation (Gazebo) clock or real wall time'
    )

    robot_description = ParameterValue(
        Command(['xacro ', model_file]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': use_sim_time}]
    )

    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', config_file]
    )

    return LaunchDescription([
        model_file_arg,
        config_file_arg,
        use_sim_time_arg,
        robot_state_publisher_node,
        joint_state_publisher_node,
        rviz_node
    ])