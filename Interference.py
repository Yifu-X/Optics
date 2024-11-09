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

# 计算颜色映射函数
def wavelength_to_rgb(wavelength):
    # 将波长映射到RGB颜色空间，这里可以选择不同的色图
    # 简单的色调映射，波长越长颜色越偏红，越短颜色偏紫
    cmap = plt.cm.plasma
    norm = Normalize(vmin=3800e-9, vmax=760e-9)  # 假设波长范围为 400nm 到 700nm
    return cmap(norm(wavelength))

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

    # 使用波长决定整体颜色色调（可以选择其他色图，如hsv）
    hue = (wavelength - 400e-9) / (700e-9 - 400e-9)  # 映射到0到1之间

    # 将波长转换为RGB色值
    rgb_color = plt.cm.hsv(hue)[:3]  # 使用HSV色图，并取前三个RGB通道

    # 使用强度调整亮度
    img.set_array(I)
    img.set_cmap('gray')  # 使用灰度色图控制亮度
    img.set_norm(Normalize(vmin=np.min(I), vmax=np.max(I)))  # 亮度归一化
    img.set_alpha(I / np.max(I))  # 根据光强调整透明度（亮度）

    # 使用颜色映射强度
    img.set_facecolor(rgb_color)  # 设置颜色映射（整体色调）
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
img = ax.imshow(I, extent=(-0.01, 0.01, -0.01, 0.01), origin='lower', cmap='gray')
plt.colorbar(img, ax=ax, label='光强')
ax.set_title('干涉图像')
ax.set_xlabel('x (m)')
ax.set_ylabel('y (m)')

# 创建输入框
ax_textbox_wl = plt.axes([0.35, 0.1, 0.3, 0.03])
textbox_wl = TextBox(ax_textbox_wl, '波长/nm', initial=str(555))

ax_textbox_d = plt.axes([0.35, 0.15, 0.3, 0.03])
textbox_d = TextBox(ax_textbox_d, '双孔间距d/mm', initial=str(0.5))

ax_textbox_z0 = plt.axes([0.35, 0.2, 0.3, 0.03])
textbox_z0 = TextBox(ax_textbox_z0, '距离z0/m', initial=str(1))

# 连接输入框的更新函数
textbox_wl.on_submit(update)
textbox_z0.on_submit(update)
textbox_d.on_submit(update)

# 显示图形
plt.show()