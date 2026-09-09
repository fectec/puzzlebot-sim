# 1. Standard Python Libraries
import os

# 2. ROS 2 Core Packages
from ament_index_python.packages import get_package_share_directory

# 3. ROS 2 Launch Libraries
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

# 4. ROS 2 Launch ROS Libraries
from launch_ros.actions import Node

def generate_launch_description():
    pkg_navigation = get_package_share_directory('puzzlebot_navigation')

    env_type     = LaunchConfiguration('env_type')
    config_file  = LaunchConfiguration('config_file')
    map_file     = LaunchConfiguration('map_file')
    use_sim_time = LaunchConfiguration('use_sim_time')

    env_type_arg = DeclareLaunchArgument(
        'env_type',
        default_value='simulation',
        description='Defines if "real" or "simulation" configuration is used'
    )

    config_file_arg = DeclareLaunchArgument(
        'config_file',
        default_value=PathJoinSubstitution([
            pkg_navigation,
            'config',
            env_type,
            'nav2.yaml'
        ]),
        description='Absolute path to the nav2 configuration YAML file'
    )

    map_file_arg = DeclareLaunchArgument(
        'map_file',
        default_value=os.path.join(
            pkg_navigation,
            'maps',
            'simulation_e80_factory.yaml'
        ),
        description='Absolute path to the map YAML file'
    )

    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='True',
        description='Use simulation (Gazebo) clock or real wall time'
    )

    nav2_map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[{
            'yaml_filename': map_file,
            'use_sim_time': use_sim_time
        }]
    )

    nav2_amcl_node = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[
            config_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    nav2_costmap_node = Node(
        package='nav2_costmap_2d',
        executable='nav2_costmap_2d',
        name='costmap',
        namespace='costmap',        
        parameters=[
            config_file,
            {'use_sim_time': use_sim_time}
        ]
    )

    nav2_lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_nav2',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'bond_timeout': 0.0,
            'node_names': ['map_server', 'amcl', 'costmap/costmap']
        }]
    )

    return LaunchDescription([
        env_type_arg,
        use_sim_time_arg,
        config_file_arg,
        map_file_arg,
        nav2_map_server_node,
        nav2_amcl_node,
        nav2_costmap_node,
        nav2_lifecycle_manager
    ])