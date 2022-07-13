export ROS_MASTER_URI=http://192.168.1.2:11311
export ROS_IP=192.168.1.92

source /opt/ros/noetic/setup.bash
nohup python3 ../mpu_6050_driver/scripts/imu_node2.py &
#nohup python3 ../mpu_6050_driver/scripts/imu_node.py &
nohup python3 ros_lidar_publisher.py &
nohup python3 ros_motor_controller.py &