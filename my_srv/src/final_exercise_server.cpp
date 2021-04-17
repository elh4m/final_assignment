#include "ros/ros.h"
#include "my_srv/final_exercise.h"

double randMToN(double M, double N)
{     return M + (rand() / ( RAND_MAX / (N-M) ) ) ; }


bool myrandom (my_srv::final_exercise::Request &req, my_srv::final_exercise::Response &res){
     res.target_index = randMToN(req.min, req.max);
     return true;
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "final_exercise_server");
  ros::NodeHandle n;
  ros::ServiceServer service= n.advertiseService("/final_exercise",myrandom);
  ros::spin();
  return 0;
}
