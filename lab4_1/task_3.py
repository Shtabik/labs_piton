import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon

plt.figure(figsize=(10, 6))
ax = plt.gca()

# ----------------------
#  Туловище голубя
# ----------------------
body = Ellipse((0, 0), 5.7, 3, color='lightgray')
ax.add_patch(body)

# ----------------------
#  Голова
# ----------------------
head = Circle((2.5, 1.2), 1.0, color='lightgray')
ax.add_patch(head)

# ----------------------
#  Глаза (большие!)
# ----------------------
eye_white_1 = Circle((2.8, 1.5), 0.32, color='white')
eye_black_1 = Circle((2.8, 1.5), 0.17, color='black')




ax.add_patch(eye_white_1)
ax.add_patch(eye_black_1)


# ----------------------
#  Клюв
# ----------------------
beak = Polygon([[3.5, 1.1], [3.85, 1.02], [3.47, 0.93]], color='orange')
ax.add_patch(beak)

# ----------------------
#  Крыло
# ----------------------
wing = Ellipse((-1, 0.3), 4.5, 2, angle=20, color='silver')
ax.add_patch(wing)

# ----------------------
#  Хвост
# ----------------------
tail = Polygon([[-3, -0.2], [-4.5, 0.7], [-4.5, -1.1]], color='gray')
ax.add_patch(tail)

# ----------------------
#  Лапки
# ----------------------
plt.plot([1, 1.2], [-1.1, -1.6], color='brown', linewidth=3)
plt.plot([2, 2.2], [-1.1, -1.6], color='brown', linewidth=3)
plt.plot([1.21,1.65], [-1.65,-1.6], color='brown', linewidth=3)
plt.plot([2.24, 2.68], [-1.65, -1.6], color='brown', linewidth=3)
plt.plot([1.2, 1.5], [-1.66, -1.8], color='brown', linewidth=3)
plt.plot([0.8, 1.2], [-1.67, -1.63], color='brown', linewidth=3)
plt.plot([2.2, 2.57], [-1.63, -1.87], color='brown', linewidth=3)
plt.plot([1.9, 2.2], [-1.67, -1.63], color='brown', linewidth=3)

# ----------------------
#  Настройки
# ----------------------
ax.set_aspect('equal')
plt.xlim(-6, 6)
plt.ylim(-3, 3)
plt.axis('off')
plt.title("Голубь", fontsize=16)

plt.show()
