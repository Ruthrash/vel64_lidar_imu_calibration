import message_filters
import rospy
import os
from std_msgs.msg import Int32, Float32

from sensor_msgs.msg import Imu, PointCloud2
from nav_msgs.msg import Odometry

pwd = '/home/autoronto/calibre_ws/src/msgs_to_file/src'

def callback(imu, gps, pcl):
  # The callback processing the pairs of numbers that arrived at approximately the same time

  #rospy.loginfo(imu.header.seq)
  #rospy.loginfo(gps.header.seq)
  #rospy.loginfo(pcl.header.seq)
  
  with open('approx_synchronous.csv', 'a+') as file:
  	file.write(
			str(imu.header.stamp.secs) + ', ' + str(imu.header.stamp.nsecs) + ', ' + str(imu.orientation.x) +  ', ' + str(imu.orientation.y) + ', ' + str(imu.orientation.z) 
+ ', ' + str(imu.orientation.w) + ', ' + str(imu.angular_velocity.x) + ', ' + str(imu.angular_velocity.y) + ', ' + str(imu.angular_velocity.z) + ', ' + str(imu.linear_acceleration.x) + ', ' + str(imu.linear_acceleration.y) + ', ' + str(imu.linear_acceleration.z) + ', ' + str(gps.pose.pose.position.x) + ', ' + str(gps.pose.pose.position.y) + ', ' + str(gps.pose.pose.position.z) + ', ' + str(gps.pose.pose.orientation.x) + ', ' + str(gps.pose.pose.orientation.y) + ', ' + str(gps.pose.pose.orientation.z) + ', ' + str(gps.pose.pose.orientation.w) + ', ' + str(gps.twist.twist.linear.x) + ', ' + str(gps.twist.twist.linear.y) + ', ' + str(gps.twist.twist.linear.z) + ', ' + str(gps.twist.twist.angular.x) + ', ' + str(gps.twist.twist.angular.y) + ', ' + str(gps.twist.twist.angular.z) + '\n'
		  )
  
  pub = rospy.Publisher('/velodyne_synced_points', PointCloud2, queue_size=100)
  pub.publish(pcl)  
  

imu_sub = message_filters.Subscriber('/imu/data', Imu)
gps_sub = message_filters.Subscriber('/navsat/odom', Odometry)
pcl_sub = message_filters.Subscriber('/velodyne_points', PointCloud2)

rospy.init_node('spot_recorder', log_level=rospy.INFO) 
ts = message_filters.ApproximateTimeSynchronizer([imu_sub, gps_sub, pcl_sub], 10, 0.1, allow_headerless=True)
ts.registerCallback(callback)
rospy.spin()
