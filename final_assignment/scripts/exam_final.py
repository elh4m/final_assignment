#! /usr/bin/env python
import rospy
from std_srvs.srv import 
import time
#To suspend excution for a specific amount of time
from time import sleep
#velocity related messages
from geometry_msgs.msg import Twist
#navigation messages
from move_base_msgs.msg import MoveBaseActionGoal
#to connect action server and action client
from actionlib_msgs.msg import GoalStatusArray
#import for custom services
from my_srv.srv import final_exercise

target_reached_status = 0



def clbk_move_base_status(msg):
    global target_reached_status
    if (len(msg.status_list) > 0):
        if msg.status_list[0].status == 3:
	        target_reached_status = 1
 

def main():
#Initializing the node(Final_code) as the sever 
    rospy.init_node('Final_code')
    global target_reached_status, wall_follower_client

    random_index_service = rospy.ServiceProxy('/final_exercise', final_exercise)
#Node used to subscribe on topic /move_base/status with a message GoalStatusArray from actionlib_msgs
    move_base_status = rospy.Subscriber('/move_base/status', GoalStatusArray, clbk_move_base_status, queue_size = 1)
#Node used to publish on topic /move_base/goal with a message MoveBaseActionGoal from move_base_msgs
    new_target_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size = 1)
#Service client used to communicate with the user interface      
    wall_follower_client = rospy.ServiceProxy('/wall_follower_switch', SetBool)
#Node used to publish on topic /cmd_vel with a message Twist from geometry_msgs
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
#Coordinates for the desired possible targets    
    random_targets = [(-4,-3), (-4,2), (-4,7), (5,-7), (5,-3), (5,1)]

    print("\nInitializing...\n")
    
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
#taking inputs from the user to perform the following tasks:
        print("""\nEnter integers from 1 to 4 to execute the following behaviors:
     (1) Move randomly in the environment, by choosing 1 out of 6 possible target positions.
     (2) Enter the next target position out of the possible six and reach it.
     (3) Start following the external walls.
     (4) To enter standby position.""")
#user's input
        x = int(input("\nEnter a number from 1 to 4 corresponding to the chosen robot behavior: "))

#When the user gives input as 1 the robot moves randomly by choosing 1 coordinate out of all possible given coordinated         
        if (x == 1):
            resp = wall_follower_client (False)
            resp = random_index_service (1,6)
            rand_index = resp.target_index

            print("\nNew Target: (" + str(random_targets[rand_index -1][0]) + ", " + str(random_targets[rand_index -1][1]) + ")")

            MoveBase_msg = MoveBaseActionGoal()
#Setting frame_id to the map            
            MoveBase_msg.goal.target_pose.header.frame_id = "map"
#here we set the orientation W             
            MoveBase_msg.goal.target_pose.pose.orientation.w = 1
#For using x as input coordinate at position x             
            MoveBase_msg.goal.target_pose.pose.position.x = random_targets[rand_index -1][0]
#For using y as input coordinate at position y 
            MoveBase_msg.goal.target_pose.pose.position.y = random_targets[rand_index -1][1]
#Publishing MoveBase_msg in type of MoveBaseActionGoal            
            new_target_pub.publish(MoveBase_msg)
#while robot is moving towards the random target
            print('\nRobot is moving towards the target position.')
            sleep(15)
            target_reached_status = 0
#the step after reaching the target
            while(target_reached_status == 0):
                sleep(1)
            print('\nRobot reached the target position.')
#When the user enters 2 as input the user interface will ask to pick a traget out of goven tragets            
        elif (x == 2):
            resp = wall_follower_client(False)

            print("""\nTarget coordinates:
            1. (-4,-3)
            2. (-4,2)
            3. (-4,7) 
            4. (5,-7)
            5. (5,-3)
            6. (5,1)""")

            user_input = int(input("\nEnter the number corresponding to the desired target coordinates: "))
            print("\nThe new target position is ("+ str(random_targets[user_input-1][0]) + ", " + str(random_targets[user_input-1][1]) + ")")

        
            MoveBase_msg = MoveBaseActionGoal()
#Setting frame_id to the map            
            MoveBase_msg.goal.target_pose.header.frame_id = "map"
#Set orientation W            
            MoveBase_msg.goal.target_pose.pose.orientation.w = 1
#For using x input for coordinate
            MoveBase_msg.goal.target_pose.pose.position.x = random_targets[user_input-1][0]
#For using y input for coordinate            
            MoveBase_msg.goal.target_pose.pose.position.y = random_targets[user_input-1][1]
#Publishing MoveBase_msg in type of MoveBaseActionGoal            
            new_target_pub.publish(MoveBase_msg)
#While robot moving towards the target
            print('\nRobot is moving towards the target position.')
            sleep(15)
            target_reached_status = 0
#After reaching the target
            while(target_reached_status == 0):
                sleep(1)
                print('\nRobot has reached the target position.')

#when the user gives input as 3 the robot starts follwing the walls which are present in the map        
        elif (x == 3):
            resp = wall_follower_client(True)
            print('\nRobot is demonstrating wall-following behavior.')
#when input is equal to 4, the velocities are set to zero the robot goes to standby mode     
        elif (x == 4):
#Function used to stop the robot by passing 0 velocity on the topic twist        
            resp = wall_follower_client(False)
            twist_msg = Twist()
            twist_msg.linear.x = 0
            twist_msg.angular.z = 0
            pub.publish(twist_msg)
            print('\nRobot has stopped.')

        else:
            continue
        
        rate.sleep()


if __name__ == '__main__':
    main()
