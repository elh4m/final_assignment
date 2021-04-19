# final_assignment by Elham Mohammadi 5073904 .research track1

The assignment is done in a ROS architecture for controling a  robot moving in the Gazebo (3D) environment.

The program is able to acquire the requests of user input:

1.Robot moves randomly by choosing 1 out of 6 possible target positions: [(-4,-3);(-4,2);(-4,7);(5,-7);(5,-3);(5,1)].

2.And asks the user for the next target position, checking that the position is one of the possible six target positions, and the robot reaches it.

3.Robot starts following  walls.

4.Robot will stop in the last position. {If the robot is in state 1 or 2, the system waits until the robot reaches the position in order to switch to state 3 or 4}.

## how the Mobile Robot is controlled:
The final_assignment package contains the scripts,launch files and other dependencies used to simulate the 3D environment and move the robot in it.The simulation_gmapping.launch file launches the house.world file environment.The importatant node exam_final.py contains python codes which is responsible for the mobile robot simulation.

The simulation is done in following steps:

1.For the first step, exam_final.py node requests my_srv for a random target position between the range of 1 to 6.When the robot reaches the target and the status of robot is displayed, the main node requests the user to input again.

2.For the second step, the user chooses 1 out of 6 possible target positions.

3.For the third step,the wall_follower service is generated through initialization of a service client to allow the robot to follow the external walls.

4.For the fourth step, the node stops all actions and stops the robot by publishing commands of zero velocity in topic /cmd_vel.

In steps 3 and 4,The interface also allows the user to enter the same or different request at any point in this state.

## my_srv(server):
The server package my_srv contains the file final_exercise_server.cpp  containing the source code for generating random integer within a specified range and advertising it over the node /final_exercise. It provides a requests with two integers namely min and max, and returns one random integer target_index within this range in response.

## Simulation of the assignment:
1.In the command terminal, launch Gazebo and rviz by executing the following command:

    roslaunch final_assignment simulation_gmapping.launch
2.in a new terminal we will run this command:

    roslaunch final_assignment move_base.launch
3.in a new terminal we will run this command:

    rosrun final_assignment wall_follow_service_m.py
4.in a new terminal we will run this command:

    rosrun my_srv final_exercise_server
5.in a new terminal we will run this command:

    rosrun final_assignment exam_final.py
6.To display the computational graph of the system,run the following command:

    rosrun rqt_graph rqt_graph
    
    
![rosgraph](https://user-images.githubusercontent.com/77781922/115144827-4b7f9100-a03e-11eb-8770-35e90c0dafe6.png)

