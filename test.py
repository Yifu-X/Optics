import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 参数
wavelength = 500e-9  # 光的波长，单位米
w = 2*np.pi*3e8/wavelength # 光的角频率
A1 = 1    # 波1的振幅
A2 = 2    # 波2的振幅
d = 1e-3            # 双孔间距，单位米
L = 1                # 屏幕距离，单位米
N = 1000             # 像素数量

# 计算
# 光源位置
source1_pos = np.array([d/2,0,0])
source2_pos = np.array([-d/2,0,0])
# 场点位置
x = np.linspace(-0.01, 0.01, N)  # 屏幕上的位置
y = np.linspace(-0.01, 0.01, N)  # 屏幕上的位置
X, Y = np.meshgrid(x, y)          # 创建网格
z0 = 0.1


# 更新函数
def update(val):
    z0 = slider.val
    d = slider_d.val
    source1_pos[0] = d / 2
    source2_pos[0] = -d / 2
    r1 = np.sqrt((X - source1_pos[0]) ** 2 + (Y - source1_pos[1]) ** 2 + z0 ** 2)
    r2 = np.sqrt((X - source2_pos[0]) ** 2 + (Y - source2_pos[1]) ** 2 + z0 ** 2)

    E = A1 / r1 * np.cos(2 * np.pi / wavelength * r1) + A2 / r2 * np.cos(2 * np.pi / wavelength * r2)
    I = E ** 2

    # 更新图像
    img.set_array(I)
    ax.draw_artist(img)
    plt.pause(0.01)

# 创建图形
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.35)

# 初始图像
r1 = np.sqrt((X - source1_pos[0])**2 + (Y - source1_pos[1])**2 + z0**2)
r2 = np.sqrt((X - source2_pos[0])**2 + (Y - source2_pos[1])**2 + z0**2)
E = A1 / r1 * np.cos(2 * np.pi / wavelength * r1) + A2 / r2 * np.cos(2 * np.pi / wavelength * r2)
I = E**2

img = ax.imshow(I, extent=(-0.01, 0.01, -0.01, 0.01), origin='lower', cmap='hot')
plt.colorbar(img, ax=ax, label='Intensity')
ax.set_title('Intensity Distribution of Interference Pattern')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# 创建滑块
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03])  # [left, bottom, width, height]
slider = Slider(ax_slider, 'z0 (m)', 0.02, 0.5, valinit=z0)
ax_slider_d = plt.axes([0.1, 0.15, 0.8, 0.03])  # d滑块位置
slider_d = Slider(ax_slider_d, 'd (m)', 0.0005, 0.002, valinit=d)

# 连接滑块的更新函数
slider.on_changed(update)
slider_d.on_changed(update)

# 显示图形
plt.show()