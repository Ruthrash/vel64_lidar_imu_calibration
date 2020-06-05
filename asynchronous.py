# import necessary packages

import message_filters
import rospy
from sensor_msgs.msg import Imu, PointCloud2
from nav_msgs.msg import Odometry


def callback(imu, gps, pcl):
  """
	[INFO] callback() function

	@params  : 
	   imu, gps, pcl : Subscriber object
  """

  global count 

  count += 1
  print('Count : '+str(count))

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

count = 0
ts.registerCallback(callback)

rospy.spin()
