import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from matplotlib.patches import Ellipse
from mpl_toolkits.axes_grid1 import make_axes_locatable

# plot setting
plt.rcParams['font.family']='Arial'

bar_width=0.25
plt.rc('axes', labelsize=11)
plt.rc('xtick', labelsize=8) 
plt.rc('ytick', labelsize=8) 
plt.rc('legend', fontsize=8)
plt.rc('figure', titlesize=10) 
title_size = 18
label_size = 14
point_alpha = 0.8

color_vs = ['#E881A6', '#6EA1D4']
color_year2 = ['#FFBE98', '#FFA74F', '#E881A6', '#60C8B3', '#6EA1D4']
color_year = ['#EFCFBA', '#FFB2A5', '#FA9A85',  '#DE8286', '#F97272']

set_dpi=300

figure_path = '../Figures/'
gpd_file_path = '../Data/'
gpd_file_name = 'sig_5179.shp'
loc_file_name = 'ASF_WildBoar_Update.csv'

location = pd.read_csv(gpd_file_path + loc_file_name)
korea = gpd.read_file(gpd_file_path + gpd_file_name)

korea = korea.to_crs(epsg=4326)

# error correction
location.loc[location['경도'].str[-2] == '.','경도'] = 128.3489
location['위도'] = location['위도'].str.replace(',', '')
location['경도'] = location['경도'].astype(float)
location['위도'] = location['위도'].astype(float)

location['확진'] = pd.to_datetime(location['확진'], format = '%Y-%m-%d')
location = location.rename(columns = {'위도' : 'y', '경도' : 'x'}, inplace  = False)

# Year
location_2019 = location.query('확진 < "2020-01-01"')
location_2020 = location.query('확진 >= "2020-01-01" & 확진 < "2021-01-01"')
location_2021 = location.query('확진 >= "2021-01-01" & 확진 < "2022-01-01"')
location_2022 = location.query('확진 >= "2022-01-01" & 확진 < "2023-01-01"')
location_2023 = location.query('확진 >= "2023-01-01" & 확진 < "2024-01-01"')

# Results for scanstatistic
korea.loc[korea['SIG_CD'] == '47280', '2022PS_cluster'] = 1

korea.loc[korea['SIG_CD'] == '47280', '2022NB_cluster'] = 1

korea.loc[korea['SIG_CD'] == '47280', '2022ZF_cluster'] = 1

korea.loc[korea['SIG_CD'] == '47920', '2022SC_cluster'] = 1

korea['2022NB_cluster'] = korea['2022NB_cluster'].fillna(0, inplace = False)
korea['2022ZF_cluster'] = korea['2022ZF_cluster'].fillna(0, inplace = False)
korea['2022PS_cluster'] = korea['2022PS_cluster'].fillna(0, inplace = False)
korea['2022SC_cluster'] = korea['2022SC_cluster'].fillna(0, inplace = False)

korea.loc[korea['SIG_CD'] == '47930', 'PS_cluster'] = 1


korea.loc[korea['SIG_CD'] == '47930', 'NB_cluster'] = 1 ## 225

korea.loc[korea['SIG_CD'] == '43150', 'ZF_cluster'] = 1
korea.loc[korea['SIG_CD'] == '43800', 'ZF_cluster'] = 1

korea.loc[korea['SIG_CD'] == '47760', 'SC_cluster'] = 2
korea.loc[korea['SIG_CD'] == '47770', 'SC_cluster'] = 2
korea.loc[korea['SIG_CD'] == '47930', 'SC_cluster'] = 2
korea.loc[korea['SIG_CD'] == '42720', 'SC_cluster'] = 1
korea.loc[korea['SIG_CD'] == '42730', 'SC_cluster'] = 1

korea['NB_cluster'] = korea['NB_cluster'].fillna(0, inplace = False)
korea['ZF_cluster'] = korea['ZF_cluster'].fillna(0, inplace = False)
korea['PS_cluster'] = korea['PS_cluster'].fillna(0, inplace = False)
korea['SC_cluster'] = korea['SC_cluster'].fillna(0, inplace = False)

location_2023_1 = location_2023.query('확진 >= "2023-01-01" & 확진 < "2023-02-01"')
location_2023_2 = location_2023.query('확진 >= "2023-02-01" & 확진 < "2023-03-01"')
location_2023_3 = location_2023.query('확진 >= "2023-03-01" & 확진 < "2023-04-01"')
location_2023_4 = location_2023.query('확진 >= "2023-04-01" & 확진 < "2023-05-01"')

location_2022_9 = location_2022.query('확진 >= "2022-09-01" & 확진 < "2022-10-01"')
location_2022_10 = location_2022.query('확진 >= "2022-10-01" & 확진 < "2022-11-01"')
location_2022_11 = location_2022.query('확진 >= "2022-11-01" & 확진 < "2022-12-01"')
location_2022_12 = location_2022.query('확진 >= "2022-12-01" & 확진 < "2023-01-01"')


most_indexes = korea.loc[korea['SIG_KOR_NM'].isin(["문경시", "충주시"]), :].index
korea.loc[most_indexes[1], '2022_most'] = 1
korea.loc[most_indexes[0], '2023_most'] = 1
korea.fillna(0, inplace = True)

most_indexes = korea.loc[korea['SIG_KOR_NM'].isin(["단양군", "영월군"]), :].index
korea.loc[most_indexes[1], '2022_model_most'] = 1
korea.loc[most_indexes[0], '2023_model_most'] = 1
korea.fillna(0, inplace = True)

korea['2022_combined'] = korea['2022_most'].astype(str) + '-' + korea['2022_model_most'].astype(str)
korea['2023_combined'] = korea['2023_most'].astype(str) + '-' + korea['2023_model_most'].astype(str)

# Figure 6
fig, ax = plt.subplots(2, 2, figsize = (12,8), dpi = set_dpi)
ax = ax.flatten()
ax1 = ax[0]; ax2 = ax[1]; ax3 = ax[2]; ax4 = ax[3]

korea.plot(column = 'PS_cluster', legend=False, ax=ax2,  cmap='Reds', edgecolor='black', linewidth = 0.5) 

korea.plot(column = '2022PS_cluster', legend=False, ax=ax1,  cmap='Reds', edgecolor='black', linewidth = 0.5)

ax2.plot(location_2023_1['x'], location_2023_1['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2023-01')
ax2.plot(location_2023_2['x'], location_2023_2['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2023-02')
ax2.plot(location_2023_3['x'], location_2023_3['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2023-03')
ax2.plot(location_2023_4['x'], location_2023_4['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2023-04')
ax2.set_facecolor('white')

ax1.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2022-09')
ax1.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2022-10')
ax1.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2022-11')
ax1.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2022-12')

# ax1.set_title('2022', fontsize = title_size)
# ax2.set_title('2023', fontsize = title_size)

ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax2.get_xaxis().set_visible(False)
ax2.get_yaxis().set_visible(False)

ax1.legend(loc = 'upper right', fontsize = 'large')
ax2.legend(loc = 'upper right', fontsize = 'large')

ax1.set_ylim([36,38.7])
ax1.set_xlim([126,129.8])
ax2.set_ylim([36,38.7])
ax2.set_xlim([126,129.8])

korea.plot(column = '2023_combined', legend=False, ax=ax4,  cmap='Blues', edgecolor='black', linewidth = 0.5) 

korea.plot(column = '2022_combined', legend=False, ax=ax3,  cmap='Blues', edgecolor='black', linewidth = 0.5)

ax4.plot(location_2023_1['x'], location_2023_1['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2023-01')
ax4.plot(location_2023_2['x'], location_2023_2['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2023-02')
ax4.plot(location_2023_3['x'], location_2023_3['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2023-03')
ax4.plot(location_2023_4['x'], location_2023_4['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2023-04')
ax4.set_facecolor('white')

ax3.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2022-09')
ax3.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2022-10')
ax3.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2022-11')
ax3.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2022-12')

# ax3.set_title('2022', fontsize = title_size)
# ax4.set_title('2023', fontsize = title_size)

ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax4.get_xaxis().set_visible(False)
ax4.get_yaxis().set_visible(False)

ax3.legend(loc = 'upper right', fontsize = 'large')
ax4.legend(loc = 'upper right', fontsize = 'large')

ax3.set_ylim([36,38.7])
ax3.set_xlim([126,129.8])
ax4.set_ylim([36,38.7])
ax4.set_xlim([126,129.8])

# ax1.set_title('2022', fontsize = title_size)
# ax2.set_title('2023', fontsize = title_size)
plt.subplots_adjust(hspace = 1)
plt.tight_layout()
# plt.savefig(image_path + 'Figure6 수정.tif', dpi = set_dpi, bbox_inches = 'tight')
plt.show()

##############################
# Figure 7
# 4*2 subplot
title_size = 30
fig, ax = plt.subplots(3, 2, figsize = (12,16), dpi = set_dpi)
ax = ax.flatten()
ax2 = ax[0]; ax1 = ax[1]; ax4 = ax[2]; ax3 = ax[3]; ax6 = ax[4]; ax5 = ax[5];


# divider = make_axes_locatable(ax1)
# cax = divider.append_axes("right",size="10%",pad="5%")
korea.plot(column = 'PS_cluster', ax=ax1, cmap='Reds', edgecolor='black')

# divider = make_axes_locatable(ax3)
# cax = divider.append_axes("right",size="10%",pad="5%")
korea.plot(column = 'NB_cluster', ax=ax3, cmap='Reds', edgecolor='black')

# divider = make_axes_locatable(ax5)
# cax = divider.append_axes("right",size="10%",pad="5%")
korea.plot(column = 'ZF_cluster', ax=ax5, cmap='Reds', edgecolor='black')


ax1.plot(location_2023_1['x'], location_2023_1['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2023-01')
ax1.plot(location_2023_2['x'], location_2023_2['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2023-02')
ax1.plot(location_2023_3['x'], location_2023_3['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2023-03')
ax1.plot(location_2023_4['x'], location_2023_4['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2023-04')

ax3.plot(location_2023_1['x'], location_2023_1['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2023-01')
ax3.plot(location_2023_2['x'], location_2023_2['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2023-02')
ax3.plot(location_2023_3['x'], location_2023_3['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2023-03')
ax3.plot(location_2023_4['x'], location_2023_4['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2023-04')

ax5.plot(location_2023_1['x'], location_2023_1['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2023-01')
ax5.plot(location_2023_2['x'], location_2023_2['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2023-02')
ax5.plot(location_2023_3['x'], location_2023_3['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2023-03')
ax5.plot(location_2023_4['x'], location_2023_4['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2023-04')


ax1.get_xaxis().set_visible(False)
ax1.get_yaxis().set_visible(False)
ax3.get_xaxis().set_visible(False)
ax3.get_yaxis().set_visible(False)
ax5.get_xaxis().set_visible(False)
ax5.get_yaxis().set_visible(False)
# ax7.get_xaxis().set_visible(False)
# ax7.get_yaxis().set_visible(False)



ax1.set_ylim([36,38.7])
ax1.set_xlim([126,129.8])
ax3.set_ylim([36,38.7])
ax3.set_xlim([126,129.8])
ax5.set_ylim([36,38.7])
ax5.set_xlim([126,129.8])
# ax7.set_ylim([36,38.7])
# ax7.set_xlim([126,129.8])

korea.plot(column = '2022PS_cluster', ax=ax2, cmap='Reds', edgecolor='black')
korea.plot(column = '2022NB_cluster', ax=ax4, cmap='Reds', edgecolor='black')
korea.plot(column = '2022ZF_cluster', ax=ax6, cmap='Reds', edgecolor='black')
# korea.plot(column = '2022SC_cluster', ax=ax8, cmap='Reds', edgecolor='black')

ax2.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2022-09')
ax2.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2022-10')
ax2.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2022-11')
ax2.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2022-12')

ax4.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2022-09')
ax4.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2022-10')
ax4.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2022-11')
ax4.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2022-12')

ax6.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 5, color = 'blue', label = '2022-09')
ax6.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 5, color = '#AAD2E4', label = '2022-10')
ax6.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 5, color = color_year[2], label = '2022-11')
ax6.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 5, color = 'red', label = '2022-12')

# ax8.plot(location_2022_9['x'], location_2022_9['y'], 'o', alpha = 0.8, markersize = 2, color = 'blue', label = '2022-09')
# ax8.plot(location_2022_10['x'], location_2022_10['y'], 'o', alpha = 0.8, markersize = 2, color = '#AAD2E4', label = '2022-10')
# ax8.plot(location_2022_11['x'], location_2022_11['y'], 'o', alpha = 0.8, markersize = 2, color = color_year[2], label = '2022-11')
# ax8.plot(location_2022_12['x'], location_2022_12['y'], 'o', alpha = 0.8, markersize = 2, color = 'red', label = '2022-12')

ax2.get_xaxis().set_visible(False)
#ax2.get_yaxis().set_visible(False)
ax2.set_yticks([])
ax4.get_xaxis().set_visible(False)
#ax4.get_yaxis().set_visible(False)
ax4.set_yticks([])
ax6.get_xaxis().set_visible(False)
#ax6.get_yaxis().set_visible(False)
ax6.set_yticks([])
# ax8.get_xaxis().set_visible(False)
#ax8.get_yaxis().set_visible(False)
# ax8.set_yticks([])

ax2.set_ylabel('PS', rotation = 90, fontsize = title_size)
ax4.set_ylabel('NB', rotation = 90, fontsize = title_size)
ax6.set_ylabel('ZIP', rotation = 90, fontsize = title_size)
# ax8.set_ylabel('SC', rotation = 90, fontsize = title_size)

ax1.legend(loc = 'upper right', fontsize = 'x-large')
ax3.legend(loc = 'upper right', fontsize = 'x-large')
ax5.legend(loc = 'upper right', fontsize = 'x-large')
# ax7.legend(loc = 'upper right', fontsize = 'x-large')

ax2.legend(loc = 'upper right', fontsize = 'x-large')
ax4.legend(loc = 'upper right', fontsize = 'x-large')
ax6.legend(loc = 'upper right', fontsize = 'x-large')
# ax8.legend(loc = 'upper right', fontsize = 'x-large')

ax2.set_ylim([36,38.7])
ax2.set_xlim([126,129.8])
ax4.set_ylim([36,38.7])
ax4.set_xlim([126,129.8])
ax6.set_ylim([36,38.7])
ax6.set_xlim([126,129.8])
# ax8.set_ylim([36,38.7])
# ax8.set_xlim([126,129.8])

ax1.set_title('2023', fontsize = title_size)
ax2.set_title('2022', fontsize = title_size)

plt.tight_layout()
# plt.savefig(image_path + 'Figure6.tif', dpi = set_dpi, bbox_inches = 'tight')
plt.show()