"""What the autograder runs on levine_obs (the obstacle course):

    ros2 launch gap_follow levine_obs_launch.py

Everything this map needs goes here: one node or several, Python or C++, and
the parameter values that suit this map (levine_blocked_launch.py is the
empty loop's). Start your own nodes only: the simulator is already running.
"""
from launch import LaunchDescription
from launch_ros.actions import Node

# 'reactive_node.py' is scripts/reactive_node.py, 'reactive_node' is the C++
# src/reactive_node.cpp: name the one you wrote
EXECUTABLE = 'reactive_node.py'

# this map's values for the parameters your node declares
# e.g. {'max_speed': 6.0} or give it a full .yaml config file
PARAMETERS = {}


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gap_follow',
            executable=EXECUTABLE,
            output='screen',
            parameters=[PARAMETERS],
        ),
    ])
