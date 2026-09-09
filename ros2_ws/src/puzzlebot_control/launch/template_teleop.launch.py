# 1. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

# 2. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock or real wall time'
    )

    template_unstamper_node = Node(
        package='twist_stamper',
        executable='twist_unstamper',
        name='template_unstamper',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        remappings=[
            ('/cmd_vel_in', '/template/cmd_vel_stamped'),
            ('/cmd_vel_out', '/template/cmd_vel')
        ]
    )

    return LaunchDescription([
        use_sim_time_arg,
        template_unstamper_node
    ])