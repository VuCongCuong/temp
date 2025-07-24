import matplotlib.pyplot as plt
import numpy as np

labels = ['Nhiệt độ', 'Ứng suất']
t_01 = [493.4, 2438.6]    # t=0.01mm
t_005 = [402.1, 2156.5]   # t=0.005mm

x = np.arange(len(labels))
width = 0.25

fig, ax_1 = plt.subplots(figsize=(8, 6))
ax_2 = ax_1.twinx()  # Tạo trục y thứ hai

bars1 = ax_1.bar(x[0] - width/2, t_01[0], width, color='#ff6f61', label='Nhiệt độ t=0.01mm')
bars2 = ax_1.bar(x[0] + width/2, t_005[0], width, color='#43c6ac', label='Nhiệt độ t=0.005mm')
bars3 = ax_2.bar(x[1] - width/2, t_01[1], width, color='#ff6f61', label='Ứng suất t=0.01mm')
bars4 = ax_2.bar(x[1] + width/2, t_005[1], width, color='#43c6ac', label='Ứng suất t=0.005mm')

ax_1.set_xticks(x)
ax_1.set_xticklabels(labels, fontsize=13)
ax_1.set_ylabel('Nhiệt độ (°C)', fontsize=14)
ax_2.set_ylabel('Ứng suất (MPa)', fontsize=14)
ax_1.set_ylim(0, 1000)
ax_2.set_ylim(0, 2700)

# Hiển thị giá trị trên đầu cột
for bar in [bars1, bars2]:
    for b in bar:
        height = b.get_height()
        ax_1.annotate(f'{height:.1f}',
                    xy=(b.get_x() + b.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)
        
for bar in [bars3, bars4]:
    for b in bar:
        height = b.get_height()
        ax_2.annotate(f'{height:.1f}',
                    xy=(b.get_x() + b.get_width() / 2, height),
                    xytext=(0, 5), textcoords="offset points",
                    ha='center', va='bottom', fontsize=12)
        

# Chú thích
fig.legend(['t = 0.01mm', 't = 0.005mm'], loc='lower center', ncol=2, fontsize=14)

plt.title('v = 30 m/s', fontsize=16, loc='center', pad=20)
plt.tight_layout()
plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()