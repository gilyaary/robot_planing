To show the lidar in rviz we need at tf broadcaster:
rosrun tf static_transform_publisher 0 0 0 0 0 0 map laser_frame  10

The laser_frame param is the ID we publish over /scan topic:
---
header: 
  seq: 213
  stamp: 
    secs: 1656237949
    nsecs: 938983201
  frame_id: "laser_frame"


  To start the lidar issue:
      rostopic pub /lidar_command std_msgs/String 'start'

  To view lidar data in terminal:
      rostopic echo scan


  To start a motor:
      rostopic pub /right_motor std_msgs/Float64 <speed>

  To See acceleration mpu6050:
      rostopic echo /imu/data


Modified impl of the imu driver.
Now publishing raw data over /imu/data_raw

We also need to convert the raw imu data to /imu/data with the following:
    rosrun imu_complementary_filter complementary_filter_node




Summary:
    1. On the orange pi just run the ros_start_all.sh
    
    2. On the "Client" pc run:
        1. start_lidar (source ~/.profile)
        2. rosrun imu_complementary_filter complementary_filter_node & 
            (converts from /imu/data_raw -> /imu/data)
        3. run conversion and correction of frames: 
           python3 ros_lidar_changer.py   
        4.  NOTE: ONLY if running for gmapping or just to view in rviz
            python3 ros_mpu_6050_tf_broadcaster.py 
            (Will create a tf frame conversion from laser_frame -> map according to the data in /imu/data we can change this later to come from odom) 
        4. rosrun rviz rviz (then open the saved config file)
        5. rosrun gmapping slam_gmapping scan:=scan   
        6. To move the robot use the   ros_robot_teleop.py

SLAM:

        7. We need to convert 0 reads to something else. So we have the process ros_lidar_changer.py
        That one just publishes on scan2 and modifies the ranges and the 0 reads

        8. To use hectorslam first modify the launch files:
             cd ~/catkin_ws/src/hector_slam/hector_slam_launch/launch
             sudo cp  ../../hector_mapping/launch/mapping_default_gil.launch    /opt/ros/noetic/share/hector_mapping/launch/
             roslaunch tutorial_gil.launch

             Or for the gmapping package:
             python3 ./ros_mpu_6050_tf_broadcaster.py
             rosrun gmapping slam_gmapping scan:=scan2 odom_frame:=odom use_sim_time:=false


            