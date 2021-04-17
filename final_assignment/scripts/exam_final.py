#! /usr/bin/env python
# importing ros stuffs
import rospy
from std_srvs.srv import *
import time
from time import sleep
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionGoal
from actionlib_msgs.msg import GoalStatusArray
from my_srv.srv import final_exercise

target_reached_status = 0



def clbk_move_base_status(msg):
    global target_reached_status
    if (len(msg.status_list) > 0):
        if msg.status_list[0].status == 3:
	        arget_reached_status = 1
 

def main():
# initializing the node(exam_final) as the server
    rospy.init_node('final_user_req')
    global target_reached_status, wall_follower_client

    random_index_service = rospy.ServiceProxy('/final_exercise', final_exercise)
#node used to subscribe on topic /move_base/status with a message GoalStatusArray from actionlib_msgs
    move_base_status = rospy.Subscriber('/move_base/status', GoalStatusArray, clbk_move_base_status, queue_size = 1)
#node used to publish on topic /move_base/goal with a message MoveBaseActionGoal from move_base_msgs
    new_target_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size = 1)
#service client used to communicate with the user interface
    wall_follower_client = rospy.ServiceProxy('/wall_follower_switch', SetBool)
#node used to publish on topic /cmd_vel with a message Twist from geometry_msg
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 1)
#coordinates for the desired possible targets
    random_targets = [(-4,-3), (-4,2), (-4,7), (5,-7), (5,-3), (5,1)]

    print("\nInitializing...\n")
    
    rate = rospy.Rate(20)
    
    while not rospy.is_shutdown():
#to take input from the user to perform 4 different tasks

        print("""\nEnter integers from 1 to 4 to execute the following behaviors:
     (1) Move randomly in the environment, by choosing 1 out of 6 possible target positions.
     (2) Enter the next target position out of the possible six and reach it.
     (3) Start following the external walls.
     (4) Stop in the last position.""")
#taking input from the user
        x = int(input("\nEnter a number from 1 to 4 corresponding to the chosen robot behavior: "))

 #when the user gives input as 1 the robot moves randonly by choosing 1 coordinate out of all possible given coordinates       
        if (x == 1):
            resp = wall_follower_client (False)
            resp = random_index_service (1,6)
            rand_index = resp.target_index

            print("\nNew Target: (" + str(random_targets[rand_index -1][0]) + ", " + str(random_targets[rand_index -1][1]) + ")")

            MoveBase_msg = MoveBaseActionGoal()
 #setting frame_id to the map
            MoveBase_msg.goal.target_pose.header.frame_id = "map"
#set orientation W            
            MoveBase_msg.goal.target_pose.pose.orientation.w = 1
#for using x as input coordinate at position x           
            MoveBase_msg.goal.target_pose.pose.position.x = random_targets[rand_index -1][0]
#for using y as input coordinate at position y
            MoveBase_msg.goal.target_pose.pose.position.y = random_targets[rand_index -1][1]
#publishing MoveBase_msg in type of MoveBaseActionGoal            
            new_target_pub.publish(MoveBase_msg)
#while robot is moving towards the random target
            print('\nRobot is moving towards the target position.')
            sleep(15)
            target_reached_status = 0
#after reaching the target
            while(target_reached_status == 0):
                sleep(1)
            print('\nRobot reached the target position.')
 #when the user enters 2 as input the user interface will ask to pick a target out of given targets           
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
#setting frame_id to the map            
            MoveBase_msg.goal.target_pose.header.frame_id = "map"
#set orientation W           
            MoveBase_msg.goal.target_pose.pose.orientation.w = 1
#for using x input for coordinate           
            MoveBase_msg.goal.target_pose.pose.position.x = random_targets[user_input-1][0]
#for using y input for coordinate            
            MoveBase_msg.goal.target_pose.pose.position.y = random_targets[user_input-1][1]
#publishing MoveBase_msg in type of MoveBaseActionGoal           
            new_target_pub.publish(MoveBase_msg)
            

            print('\nRobot is moving towards the target position.')
            sleep(15)
            target_reached_status = 0

            while(target_reached_status == 0):
                sleep(1)
                print('\nRobot has reached the target position.')

#when the user gives input as 3 the robot starts following the walls which are present in the map        
        elif (x == 3):
            resp = wall_follower_client(True)
            print('\nRobot is demonstrating wall-following behavior.')
#when input is equal to 4 the velocities are set to zero the robot goes to standby mode            
        elif (x == 4):
#function used to stop the robot by passing 0 velocity on the topic Twist        
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
