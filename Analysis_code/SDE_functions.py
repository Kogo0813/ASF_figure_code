## Function to plot the ellipse
from matplotlib.patches import Ellipse
import numpy as np

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
    from matplotlib.patches import Ellipse
    elp = Ellipse(xy = mean, width = np.sqrt(cov[0,0]) * 2,
                height = np.sqrt(cov[1,1]) * 2,
                angle = np.rad2deg(np.arccos(cov[0,1] / np.sqrt(cov[0,0] * cov[1,1]))),
                edgecolor = 'black', facecolor = color, alpha = 0.5, linewidth = 0.7)
    return elp

def confidence_ellipse_info(x, y, ax, n_std=2.0, facecolor='none', **kwargs):
    import matplotlib.transforms as transforms
    from matplotlib.patches import Ellipse
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


