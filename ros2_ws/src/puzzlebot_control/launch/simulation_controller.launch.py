# 1. ROS 2 Launch Libraries
from launch import LaunchDescription

# 2. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node

def generate_launch_description():
    joint_state_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_drive_controller"],
    )

    forks_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["forks_controller"],
    )

    return LaunchDescription([
        joint_state_spawner,
        diff_drive_spawner,
        forks_spawner
    ])