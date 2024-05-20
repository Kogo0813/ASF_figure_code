import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from matplotlib.patches import Ellipse

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

mean_2019 = np.array([np.mean(location_2019['x']), np.mean(location_2019['y'])])
cov_2019 = np.cov(location_2019['x'], location_2019['y'])

mean_2020 = np.array([np.mean(location_2020['x']), np.mean(location_2020['y'])])
cov_2020 = np.cov(location_2020['x'], location_2020['y'])

mean_2021 = np.array([np.mean(location_2021['x']), np.mean(location_2021['y'])])
cov_2021 = np.cov(location_2021['x'], location_2021['y'])

mean_2022 = np.array([np.mean(location_2022['x']), np.mean(location_2022['y'])])
cov_2022 = np.cov(location_2022['x'], location_2022['y'])

mean_2023 = np.array([np.mean(location_2023['x']), np.mean(location_2023['y'])])
cov_2023 = np.cov(location_2023['x'], location_2023['y'])

## Function to plot the ellipse
def confidence_ellipse(x, y, ax, n_std=2.0, facecolor='none', **kwargs):
    import matplotlib.transforms as transforms
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    # Using a special case to obtain the eigenvalues of this
    # two-dimensional dataset.
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, edgecolor = 'black', **kwargs, alpha = 0.3, linewidth = 0.7)

    # Calculating the standard deviation of x from
    # the squareroot of the variance and multiplying
    # with the given number of standard deviations.
    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    # calculating the standard deviation of y ...
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

def speed_ellipse(x, y, n_std = 2.0, facecolor = 'none', **kwargs):
    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    width = ell_radius_x * 2
    height = ell_radius_y * 2

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    # 타원의 각도를 추출
    angle = np.arctan2(cov[0,0], cov[0,1])
    angle = np.degrees(angle)
    return pd.DataFrame({'width' : width, 'height' : height, 'scale_x' : scale_x, 'scale_y' : scale_y, 'mean_x' : mean_x, 'mean_y' : mean_y, 'angle' : angle}, index = [0])

def Make_ellipse(mean, cov, color):
    elp = Ellipse(xy = mean, width = np.sqrt(cov[0,0]) * 2,
                height = np.sqrt(cov[1,1]) * 2,
                angle = np.rad2deg(np.arccos(cov[0,1] / np.sqrt(cov[0,0] * cov[1,1]))),
                edgecolor = 'black', facecolor = color, alpha = 0.5, linewidth = 0.7)
    return elp

def confidence_ellipse_info(x, y, ax, n_std=2.0, facecolor='none', **kwargs):
    import matplotlib.transforms as transforms
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)
    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    ax.add_patch(ellipse)
    
    # 필요한 정보 반환
    return mean_x, mean_y, cov, ell_radius_x * 2, ell_radius_y * 2, 45

# Figure 5
ellipse_2019 = Make_ellipse(mean_2019, cov_2019, color_year2[0])
ellipse_2020 = Make_ellipse(mean_2020, cov_2020, color_year2[1])
ellipse_2021 = Make_ellipse(mean_2021, cov_2021, color_year2[2])
ellipse_2022 = Make_ellipse(mean_2022, cov_2022, color_year2[3])
ellipse_2023 = Make_ellipse(mean_2023, cov_2023, color_year2[4])

fig, ax = plt.subplots(1, 1, figsize = (12, 8), dpi = set_dpi)
korea.plot(ax = ax, color = 'white', edgecolor = 'black', alpha = 0.6)
ax.scatter(location_2019['x'], location_2019['y'], s = 1, color = color_year2[0], alpha = point_alpha, label = '2019')
ax.scatter(location_2020['x'], location_2020['y'], s = 1, color = color_year2[1], alpha = point_alpha, label = '2020')
ax.scatter(location_2021['x'], location_2021['y'], s = 1, color = color_year2[2], alpha = point_alpha, label = '2021')
ax.scatter(location_2022['x'], location_2022['y'], s = 1, color = color_year2[3], alpha = point_alpha, label = '2022')
ax.scatter(location_2023['x'], location_2023['y'], s = 1, color = color_year2[4], alpha = point_alpha, label = '2023')

confidence_ellipse(location_2019['x'], location_2019['y'], ax, n_std=2.0, facecolor=color_year2[0])
confidence_ellipse(location_2020['x'], location_2020['y'], ax, n_std=2.0, facecolor=color_year2[1])
confidence_ellipse(location_2021['x'], location_2021['y'], ax, n_std=2.0, facecolor=color_year2[2])
confidence_ellipse(location_2022['x'], location_2022['y'], ax, n_std=2.0, facecolor=color_year2[3])
confidence_ellipse(location_2023['x'], location_2023['y'], ax, n_std=2.0, facecolor=color_year2[4])

ax.legend()

ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

ax.set_title('Points of ASFV cases in South Korea', fontsize = title_size)
# plt.savefig(image_path + 'Figure5.tif', dpi = set_dpi, bbox_inches = 'tight')
plt.show()
