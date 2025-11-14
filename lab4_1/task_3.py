import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Polygon

plt.figure(figsize=(10, 6))
ax = plt.gca()

# ----------------------
#  Туловище голубя
# ----------------------
body = Ellipse((0, 0), 6, 3, color='lightgray')
ax.add_patch(body)

# ----------------------
#  Голова
# ----------------------
head = Circle((2.5, 1.2), 1.0, color='lightgray')
ax.add_patch(head)

# ----------------------
#  Глаза (большие!)
# ----------------------
eye_white_1 = Circle((3.0, 1.5), 0.45, color='white')
eye_black_1 = Circle((3.0, 1.5), 0.18, color='black')

eye_white_2 = Circle((2.0, 1.5), 0.45, color='white')
eye_black_2 = Circle((2.0, 1.5), 0.18, color='black')

ax.add_patch(eye_white_1)
ax.add_patch(eye_black_1)

ax.add_patch(eye_white_2)
ax.add_patch(eye_black_2)

# ----------------------
#  Клюв
# ----------------------
beak = Polygon([[3.5, 1.1], [4.2, 1.0], [3.5, 0.9]], color='orange')
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

# ----------------------
#  Настройки
# ----------------------
ax.set_aspect('equal')
plt.xlim(-6, 6)
plt.ylim(-3, 3)
plt.axis('off')
plt.title("Голубь", fontsize=16)

plt.show()
