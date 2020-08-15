from pypcd import pypcd 
import csv 
import numpy 
import glob as glob
import matplotlib.pyplot as plt
import pprint 
from mpl_toolkits.mplot3d import Axes3D 
import tf 
csv_file = "/home/ruthz/aer1514_ws/src/vel64_lidar_imu_calibration/approx_synchronous.csv"
pcd_base_dir = "/media/ruthz/data/pcds"
line_count = 0


pcd_files = glob.glob(pcd_base_dir+'/*.pcd')
pcd_files.sort()



beam_a = []
traj = []
trans_vel_2_imu = [0.000, 0.046, 0.399]
rot_vel_2_imu =  [0.000, 0.000, 0.707, 0.707]
trans_mat = tf.transformations.translation_matrix(trans_vel_2_imu)
rot_mat    = tf.transformations.quaternion_matrix(rot_vel_2_imu)
T_vel_2_imu = numpy.dot(trans_mat, rot_mat)
flag = True
itera = 0
fig = plt.figure()
ax1 = fig.add_subplot(111)
with open(csv_file,'rt')as f:
	data = csv.reader(f)
	for pcd_file,row in zip(pcd_files,data):
		quaternion = (row[15],row[16],row[17],row[18])
		#rot = tf.transformations.euler_from_quaternion(quaternion)
		trans = (row[12],row[13],row[14])
		trans_mat = tf.transformations.translation_matrix(trans)
		rot_mat    = tf.transformations.quaternion_matrix(quaternion)
		T_imu_2_odom = numpy.dot(trans_mat,rot_mat)
		T_vel_2_odom = numpy.dot(T_imu_2_odom, T_vel_2_imu)
		if(flag):
			init = tf.transformations.inverse_matrix(T_vel_2_odom)
			flag = False
		T_vel_2_init = numpy.dot(init, T_vel_2_odom)
		print(T_vel_2_init)
		cloud = pypcd.PointCloud.from_path(pcd_file)
		points = (cloud.pc_data['x'],cloud.pc_data['y'],cloud.pc_data['z'],numpy.ones(cloud.pc_data['z'].shape))
		new_points = numpy.dot(T_vel_2_init,points)
		tmp = numpy.c_[new_points[0], new_points[1], new_points[2]]
		if(beam_a == []):
			beam_a = numpy.r_[tmp]
		else:
			beam_a = numpy.r_[beam_a,tmp]
		
		#beam_no = 31
		#np_array = numpy.array(cloud.pc_data['ring'])
		#item_index = numpy.where(cloud.pc_data['ring']==beam_no)

		#points = (cloud.pc_data['x'][item_index],cloud.pc_data['y'][item_index],cloud.pc_data['z'][item_index],numpy.ones(cloud.pc_data['z'][item_index].shape))
		#new_points = numpy.dot(T_vel_2_init,points)
	

		#tmp = numpy.c_[new_points[0], new_points[1]]
		#if(beam_a == []):
		#	beam_a = numpy.r_[tmp]
		#else:
		#	beam_a = numpy.r_[beam_a,tmp]






































		#tmp1 =  numpy.c_[T_vel_2_init[0,3], T_vel_2_init[1,3], T_vel_2_init[2,3]]
		#if(traj == []):
		#	traj = numpy.r_[tmp1]
		#else:
		#	traj = numpy.r_[traj,tmp1]
			
			#plt.scatter(new_points[0][item_index], new_points[1][item_index])
		
		
		


		#cloud = pypcd.PointCloud.from_path(pcd_file)
		#np_array = np.array(cloud.pc_data['ring'])
		#beam_no_a = 31
		#beam_no_b = 32
		#item_index = np.where(np_array==beam_no_a)
	




cloud = pypcd.PointCloud.from_path(pcd_files[0])
cloud_1 = pypcd.PointCloud.from_path(pcd_files[1])
cloud_2 = pypcd.PointCloud.from_path(pcd_files[2])

#prints metadata of pcd 
pprint.pprint(cloud.get_metadata())


np_array = numpy.array(cloud.pc_data['ring'])
np_array_1 = np.array(cloud_1.pc_data['ring'])
np_array_2 = np.array(cloud_2.pc_data['ring'])
beam_no = 31
item_index = numpy.where(np_array==beam_no)
item_index_1 = np.where(np_array_1==beam_no)
item_index_2 = np.where(np_array_2==beam_no)


##plots xy cordinates of PCD 
plt.scatter(cloud.pc_data['x'][item_index], cloud.pc_data['y'][item_index],color='red')
plt.scatter(cloud_1.pc_data['x'][item_index_1], cloud_1.pc_data['y'][item_index_1],color='blue')
plt.scatter(cloud_2.pc_data['x'][item_index_2], cloud_2.pc_data['y'][item_index_2],color='green')
plt.show()







fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cloud.pc_data['x'], cloud.pc_data['y'], cloud.pc_data['z'])
