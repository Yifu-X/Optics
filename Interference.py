import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable

# 全局单位m

# 设置全局字体为微软雅黑
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 参数
wavelength = 555e-9  # 光的波长
w = 2*np.pi*3e8/wavelength # 光的角频率
A1 = 1    # 波1的振幅
A2 = 1    # 波2的振幅
d = 5e-4    # 双孔间距
N = 1000    # 像素数量

# 光源位置
source1_pos = np.array([d/2,0,0])
source2_pos = np.array([-d/2,0,0])

# 场点位置
x = np.linspace(-0.1, 0.1, N)  # 屏幕上的位置
y = np.linspace(-0.1, 0.1, N)  # 屏幕上的位置
X, Y = np.meshgrid(x, y)          # 创建网格
z0 = 1

# 更新参数
def update(val):
    try:
        wavelength = float(textbox_wl.text)/1e9    # 输入单位nm，转为m
        z0 = float(textbox_z0.text)
        d = float(textbox_d.text)/1000  # 输入单位mm，转为m
    except ValueError:
        return  # 如果输入的不是有效数值，则返回，不更新

    source1_pos[0] = d / 2
    source2_pos[0] = -d / 2
    r1 = np.sqrt((X - source1_pos[0]) ** 2 + (Y - source1_pos[1]) ** 2 + z0 ** 2)
    r2 = np.sqrt((X - source2_pos[0]) ** 2 + (Y - source2_pos[1]) ** 2 + z0 ** 2)

    I = A1**2 + A2**2 + 2*A1*A2*np.cos(2*np.pi/wavelength*(r1-r2))

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
I = A1**2 + A2**2 + 2*A1*A2*np.cos(2*np.pi/wavelength*(r1-r2))

# 初始的颜色映射
img = ax.imshow(I, extent=(-0.01, 0.01, -0.01, 0.01), origin='lower', cmap='hot')
plt.colorbar(img, ax=ax, label='光强')
ax.set_title('干涉图像')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# 创建输入框
ax_textbox_wl = plt.axes([0.35, 0.1, 0.1, 0.03])
textbox_wl = TextBox(ax_textbox_wl, '波长/nm', initial=str(555))

ax_textbox_d = plt.axes([0.35, 0.15, 0.1, 0.03])
textbox_d = TextBox(ax_textbox_d, '双孔间距d/mm', initial=str(0.5))

ax_textbox_z0 = plt.axes([0.35, 0.2, 0.1, 0.03])
textbox_z0 = TextBox(ax_textbox_z0, '距离z0/m', initial=str(1))

# 连接输入框的更新函数
textbox_wl.on_submit(update)
textbox_z0.on_submit(update)
textbox_d.on_submit(update)

# 显示图形
plt.show()