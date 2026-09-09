# 1. ROS 2 Core Packages
from ament_index_python.packages import get_package_share_directory

# 2. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

# 3. ROS 2 Launch ROS Libraries

from launch_ros.actions import Node
def generate_launch_description():
    pkg_control = get_package_share_directory('puzzlebot_control')

    env_type = LaunchConfiguration('env_type')
    config_file = LaunchConfiguration('config_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    env_type_arg = DeclareLaunchArgument(
        'env_type',
        default_value='simulation',
        description='Defines if "real" or "simulation" configuration is used'
    )

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=PathJoinSubstitution([pkg_control, 'config', env_type, 'joystick_teleop.yaml']),
        description='Absolute path to the joystick teleop configuration YAML file'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock or real wall time'
    )

    joy_node = Node(
        package='joy',
        executable='joy_node',
        name='joy',
        parameters=[
            config_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    joy_teleop_node = Node(
        package='joy_teleop',
        executable='joy_teleop',
        name='joy_teleop',
        parameters=[
            config_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    joy_twist_unstamper_node = Node(
        package='twist_stamper',
        executable='twist_unstamper',
        name='joy_twist_unstamper',
        parameters=[{'use_sim_time': use_sim_time}],
        remappings=[
            ('/cmd_vel_in', '/joy_teleop/cmd_vel_stamped'),
            ('/cmd_vel_out', '/joy_teleop/cmd_vel')
        ]
    )

    return LaunchDescription([
        env_type_arg,
        config_file_arg,
        use_sim_time_arg,
        joy_node,
        joy_teleop_node,
        joy_twist_unstamper_node
    ])