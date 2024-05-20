import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

figure_path = '../Figures/'
gpd_file_path = '../Data/'
gpd_file_name = 'sig_5179.shp'

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

def assign_color(val):
    if 1 <= val <= 4 or val >= 11:
        return color_vs[0]
    else:
        return color_vs[1]

# color setting
color_vs = ['#E881A6', '#6EA1D4']
color_year2 = ['#FFBE98', '#FFA74F', '#E881A6', '#60C8B3', '#6EA1D4']
color_year = ['#EFCFBA', '#FFB2A5', '#FA9A85',  '#DE8286', '#F97272']

set_dpi=300

location = pd.read_csv(gpd_file_path + 'ASF_WildBoar_Update.csv')

# error correction
location.loc[location['경도'].str[-2] == '.','경도'] = 128.3489
location['위도'] = location['위도'].str.replace(',', '')
location['경도'] = location['경도'].astype(float)
location['위도'] = location['위도'].astype(float)

location['확진'] = pd.to_datetime(location['확진'], format = '%Y-%m-%d')
location = location.rename(columns = {'위도' : 'y', '경도' : 'x'}, inplace  = False)

location_2019 = location.query('확진 < "2020-01-01"')
location_2020 = location.query('확진 >= "2020-01-01" & 확진 < "2021-01-01"')
location_2021 = location.query('확진 >= "2021-01-01" & 확진 < "2022-01-01"')
location_2022 = location.query('확진 >= "2022-01-01" & 확진 < "2023-01-01"')
location_2023 = location.query('확진 >= "2023-01-01" & 확진 < "2024-01-01"')

location_2020['month'] = location_2020['확진'].dt.month
location_2021['month'] = location_2021['확진'].dt.month
location_2022['month'] = location_2022['확진'].dt.month

list_2020 = location_2020.groupby('month').size()
list_2021 = location_2021.groupby('month').size()
list_2022 = location_2022.groupby('month').size()

cum_values = location.groupby('확진').size().cumsum()
cum_values_days = location.groupby('확진').size()
df_cum = pd.DataFrame({'date' : cum_values_days.index, 'value' : cum_values_days.values})
ind = pd.date_range(start = '2019-11-01', end = '2023-05-01')
test_df = pd.DataFrame({'date' : ind})
test_df = pd.merge(test_df, df_cum, left_on = 'date', right_on = 'date', how = 'left').fillna(0)
cum_values_days = test_df['value']
cum_values_days.index = test_df['date']

start_date_2019 = pd.to_datetime('2019-11-01')
end_date_2019 = pd.to_datetime('2020-04-30')

start_date_2020 = pd.to_datetime('2020-05-01')
end_date_2020 = pd.to_datetime('2020-10-31')

start_date_2020_2 = pd.to_datetime('2020-11-01')
end_date_2020_2 = pd.to_datetime('2021-04-30')

start_date_2021 = pd.to_datetime('2021-05-01')
end_date_2021 = pd.to_datetime('2021-10-31')

start_date_2021_2 = pd.to_datetime('2021-11-01')
end_date_2021_2 = pd.to_datetime('2022-04-30')

start_date_2022 = pd.to_datetime('2022-05-01')
end_date_2022 = pd.to_datetime('2022-10-31')

start_date_2022_2 = pd.to_datetime('2022-11-01')
end_date_2022_2 = pd.to_datetime('2023-04-30')

start_date_2023 = pd.to_datetime('2023-05-01')
end_date_2023 = pd.to_datetime('2023-10-31')

# Figure 3
title_size = 24
fig = plt.figure(figsize = (18, 9), dpi = set_dpi)

gs1_nrows = 1
gs1_ncols = 2
gs1 = fig.add_gridspec(gs1_nrows, gs1_ncols, bottom = 0.6, top = 1)

ax4 = fig.add_subplot(gs1[0, 0])
ax5 = fig.add_subplot(gs1[0, 1])

ax4.set_xlim([start_date_2019, pd.to_datetime('2023-07-01')])
# ax4.set_ylim([])

# ax4.plot(cum_values_days.index, cum_values_days.values, color = 'black', linewidth = 1, linestyle = '--', alpha = 0.8, marker = 'o', markersize = 1)
ax4.axvline(x = start_date_2019, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2019, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2020, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2020_2, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2021, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2021_2, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2022, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2022_2, color = 'gray', linestyle = '--', linewidth = 1)
ax4.axvline(x = end_date_2023, color = 'gray', linestyle = '--', linewidth = 1)

ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2019) & (cum_values_days.index <= end_date_2019), color = color_vs[0], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2020) & (cum_values_days.index <= end_date_2020), color = color_vs[1], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2020_2) & (cum_values_days.index <= end_date_2020_2), color = color_vs[0], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2021) & (cum_values_days.index <= end_date_2021), color = color_vs[1], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2021_2) & (cum_values_days.index <= end_date_2021_2), color = color_vs[0], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2022) & (cum_values_days.index <= end_date_2022), color = color_vs[1], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2022_2) & (cum_values_days.index <= end_date_2022_2), color = color_vs[0], alpha = 0.4)
ax4.fill_between(cum_values_days.index, cum_values_days.values, where = (cum_values_days.index >= start_date_2023) & (cum_values_days.index <= end_date_2023), color = color_vs[1], alpha = 0.4)



ax4.set_xticks([start_date_2019, end_date_2019, end_date_2020, end_date_2020_2, end_date_2021, end_date_2021_2, end_date_2022, end_date_2022_2])
labels = [date.strftime('%Y-%m') for date in [start_date_2019, end_date_2019, end_date_2020, end_date_2020_2, end_date_2021, end_date_2021_2, end_date_2022, end_date_2022_2]]
ax4.set_xticklabels(labels)

ax4.set_xlabel('Date', fontsize = label_size)
ax4.set_ylabel('Number of cases', fontsize = label_size)
ax4.set_title('Daily number of ASFV cases', fontsize = title_size)

red_patch = mpatches.Patch(color=color_vs[0], label='AT season', alpha = 0.7)
blue_patch = mpatches.Patch(color=color_vs[1], label='IT season', alpha = 0.7)

ax4.legend(handles=[red_patch, blue_patch], loc='upper left', fontsize='large')

# x축 레이블 회전 (옵션)
ax4.tick_params(axis='x', rotation=45)

ax5.set_xlim([start_date_2019, pd.to_datetime('2023-07-01')])
ax5.set_ylim([0, 3400])

ax5.plot(cum_values.index, cum_values.values, color = 'black', linewidth = 1, linestyle = '--', alpha = 0.8, marker = 'o', markersize = 2)
ax5.axvline(x = start_date_2019, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2019, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2020, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2020_2, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2021, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2021_2, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2022, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2022_2, color = 'gray', linestyle = '--', linewidth = 1)
ax5.axvline(x = end_date_2023, color = 'gray', linestyle = '--', linewidth = 1)

ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2019) & (cum_values.index <= end_date_2019), color = color_vs[0], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2020) & (cum_values.index <= end_date_2020), color = color_vs[1], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2020_2) & (cum_values.index <= end_date_2020_2), color = color_vs[0], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2021) & (cum_values.index <= end_date_2021), color = color_vs[1], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2021_2) & (cum_values.index <= end_date_2021_2), color = color_vs[0], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2022) & (cum_values.index <= end_date_2022), color = color_vs[1], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2022_2) & (cum_values.index <= end_date_2022_2), color = color_vs[0], alpha = 0.4)
ax5.fill_between(cum_values.index, cum_values.values, where = (cum_values.index >= start_date_2023) & (cum_values.index <= end_date_2023), color = color_vs[1], alpha = 0.4)



ax5.set_xticks([start_date_2019, end_date_2019, end_date_2020, end_date_2020_2, end_date_2021, end_date_2021_2, end_date_2022, end_date_2022_2])
labels = [date.strftime('%Y-%m') for date in [start_date_2019, end_date_2019, end_date_2020, end_date_2020_2, end_date_2021, end_date_2021_2, end_date_2022, end_date_2022_2]]
ax5.set_xticklabels(labels)

ax5.set_xlabel('Date', fontsize = label_size)
ax5.set_ylabel('Number of cases', fontsize = label_size)
ax5.set_title('Cumulative number of ASF cases', fontsize = title_size)

red_patch = mpatches.Patch(color=color_vs[0], label='AT season', alpha = 0.7)
blue_patch = mpatches.Patch(color=color_vs[1], label='IT season', alpha = 0.7)

ax5.legend(handles=[red_patch, blue_patch], loc='upper left', fontsize='large')

# x축 레이블 회전 (옵션)
ax5.tick_params(axis='x', rotation=45)

#################
gs2_nrows = 1
gs2_ncols = 3
gs2 = fig.add_gridspec(gs2_nrows, gs2_ncols, bottom = 0, top = 0.45)

ax1 = fig.add_subplot(gs2[0, 0])
ax2 = fig.add_subplot(gs2[0, 1])
ax3 = fig.add_subplot(gs2[0, 2])

red_patch = mpatches.Patch(color=color_vs[0], label='AT season', alpha = 0.7)
blue_patch = mpatches.Patch(color=color_vs[1], label='IT season', alpha = 0.7)

sns.barplot(x = list_2020.index, y = list_2020.values, ax = ax1, palette = [assign_color(i) for i in list_2020.index], alpha = 0.7)
ax1.axhline(y = np.mean(list_2020.values), color = 'red', linestyle = '--', linewidth = 2)
ax1.plot(list_2020.index-1, list_2020.values, color='black', linewidth=1, linestyle='--', alpha=0.8, marker = 'o', markersize = 3)
ax1.text(5, np.mean(list_2020.values) + 5, 'MEAN', fontsize=8)
ax1.set_xlabel('Month', fontsize = label_size)
ax1.set_ylabel('Number of cases', fontsize = label_size)
ax1.set_title('2020', fontsize = title_size)

sns.barplot(x = list_2021.index, y = list_2021.values, ax = ax2, palette = [assign_color(i) for i in list_2021.index], alpha = 0.7)
ax2.axhline(y = np.mean(list_2021.values), color = 'red', linestyle = '--', linewidth = 2)
ax2.plot(list_2021.index-1, list_2021.values, color='black', linewidth=1, linestyle='--', alpha=0.8, marker = 'o', markersize = 3)
ax2.text(5, np.mean(list_2021.values) + 5, 'MEAN', fontsize=8)
ax2.set_xlabel('Month', fontsize = label_size)
ax2.set_ylabel('Number of cases', fontsize = label_size)
ax2.set_title('2021', fontsize = title_size)

sns.barplot(x = list_2022.index, y = list_2022.values, ax = ax3, palette = [assign_color(i) for i in list_2022.index], alpha = 0.7)
ax3.axhline(y = np.mean(list_2022.values), color = 'red', linestyle = '--', linewidth = 2)
ax3.plot(list_2022.index-1, list_2022.values, color='black', linewidth=1, linestyle='--', alpha=0.8, marker = 'o', markersize = 3)
ax3.text(5, np.mean(list_2022.values) + 5, 'MEAN', fontsize=8)
ax3.set_xlabel('Month', fontsize = label_size)
ax3.set_ylabel('Number of cases', fontsize = label_size)
ax3.set_title('2022', fontsize = title_size)

# 범례 추가
ax1.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize='large')
ax2.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize='large')
ax3.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize='large')

plt.tight_layout()
# plt.savefig(image_path + 'Figure1+2.tif', dpi = set_dpi, bbox_inches = 'tight')
plt.show()