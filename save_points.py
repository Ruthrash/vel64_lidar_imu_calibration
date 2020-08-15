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

pcd_files = glob.glob(pcd_base_dir+'/*.pcd')
pcd_files.sort()

itera = 0
for pcd_file in pcd_files:
	cloud = pypcd.PointCloud.from_path(pcd_file)
	np_array = numpy.array(cloud.pc_data['ring'])
	for beam_no in range(64):
		item_index = numpy.where(cloud.pc_data['ring']==beam_no)
		a = ( np.ones(len(cloud.pc_data['x'][item_index]))*itera, cloud.pc_data['x'][item_index],cloud.pc_data['y'][item_index],cloud.pc_data['z'][item_index])
		a = numpy.array(a)
		with open('/home/ruthz/Desktop/beams/beam_'+ str(beam_no) + '.csv',"ab") as f:
			numpy.savetxt(f, a.T, delimiter=",")
	print(itera,len(pcd_files))
	itera = itera + 1 
			






			
	
