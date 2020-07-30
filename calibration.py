from pypcd import pypcd 
import csv 
import numpy 
import glob as glob
import matplotlib.pyplot as plt
import pprint 
from mpl_toolkits.mplot3d import Axes3D 

csv_file = "/home/ruthz/aer1514_ws/src/vel64_lidar_imu_calibration/approx_synchronous.csv"
pcd_base_dir = "/media/ruthz/data/pcds/"
line_count = 0
with open(csv_file,'rt')as f:
  data = csv.reader(f)
  for row in data:
        print(row)

pcd_files = glob.glob(pcd_base_dir+'/*.pcd')
pcd_files.sort()


cloud = pypcd.PointCloud.from_path(pcd_files[0])

#prints metadata of pcd 
pprint.pprint(cloud.get_metadata())

##plots xy cordinates of PCD 
plt.scatter(cloud.pc_data['x'], cloud.pc_data['y'])
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cloud.pc_data['x'], cloud.pc_data['y'], cloud.pc_data['z'])