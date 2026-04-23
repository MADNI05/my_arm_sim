import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg_name = 'my_arm_sim'
    
    # Charger l'URDF via Xacro
    urdf_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'arm.urdf.xacro')
    robot_description_config = xacro.process_file(urdf_path)
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': True}

    return LaunchDescription([
        # 1. Gazebo Sim
        ExecuteProcess(cmd=['gz', 'sim', '-r', 'empty.sdf'], output='screen'),

        # 2. Robot State Publisher
        Node(package='robot_state_publisher', executable='robot_state_publisher', output='screen', parameters=[params]),

        # 3. Spawn du robot dans Gazebo
        Node(package='ros_gz_sim', executable='create', arguments=['-topic', 'robot_description', '-name', 'arm_robot'], output='screen'),

        # 4. Spawner des contrôleurs (chargés APRES le spawn du robot)
        Node(package='controller_manager', executable='spawner', arguments=['joint_state_broadcaster']),
        Node(package='controller_manager', executable='spawner', arguments=['arm_controller']),
        
        # 5. RViz2
        Node(package='rviz2', executable='rviz2', output='screen')
    ])
