"""
Interactive 3D viewer for Question 1c & 1d.
Run this script and use your mouse to rotate the 3D plot:
  - Left-click + drag to rotate
  - Right-click + drag to zoom
  - Middle-click + drag to pan
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(14, 9))
ax = fig.add_subplot(111, projection='3d')
fig.suptitle("Question 1c & 1d: 3D Rotations (Interactive)", fontsize=14, fontweight='bold')

p = np.array([2, 4, 2])

# --- Compute rotations ---
# Step 1: Rz(pi/2)
theta_z = np.pi / 2
Rz = np.array([[np.cos(theta_z), -np.sin(theta_z), 0],
               [np.sin(theta_z),  np.cos(theta_z), 0],
               [0,                0,                1]])
p_after_rz = Rz @ p  # [-4, 2, 2]

# Step 2: Ry(-pi/4)
theta_y = -np.pi / 4
Ry = np.array([[ np.cos(theta_y), 0, np.sin(theta_y)],
               [ 0,               1, 0              ],
               [-np.sin(theta_y), 0, np.cos(theta_y)]])
q = Ry @ p_after_rz  # final point

# --- Draw coordinate axes ---
axis_len = 6
ax.quiver(0, 0, 0, axis_len, 0, 0, color='r', arrow_length_ratio=0.05, linewidth=2, label='x-axis')
ax.quiver(0, 0, 0, 0, axis_len, 0, color='g', arrow_length_ratio=0.05, linewidth=2, label='y-axis')
ax.quiver(0, 0, 0, 0, 0, axis_len, color='b', arrow_length_ratio=0.05, linewidth=2, label='z-axis')
ax.text(axis_len + 0.3, 0, 0, 'X', fontsize=14, color='r', fontweight='bold')
ax.text(0, axis_len + 0.3, 0, 'Y', fontsize=14, color='g', fontweight='bold')
ax.text(0, 0, axis_len + 0.3, 'Z', fontsize=14, color='b', fontweight='bold')

# --- Draw negative axes (dashed) ---
ax.plot([0, -axis_len], [0, 0], [0, 0], 'r--', alpha=0.2, linewidth=1)
ax.plot([0, 0], [0, -axis_len], [0, 0], 'g--', alpha=0.2, linewidth=1)
ax.plot([0, 0], [0, 0], [0, -axis_len], 'b--', alpha=0.2, linewidth=1)

# --- Point p (original) ---
ax.scatter(*p, color='purple', s=150, zorder=5)
ax.text(p[0] + 0.3, p[1] + 0.3, p[2] + 0.3,
        f'p = [{p[0]:.0f}, {p[1]:.0f}, {p[2]:.0f}]',
        fontsize=11, color='purple', fontweight='bold')
ax.quiver(0, 0, 0, p[0], p[1], p[2], color='purple', arrow_length_ratio=0.04,
          linewidth=2, alpha=0.6)

# --- Point p' (after Rz(pi/2)) ---
ax.scatter(*p_after_rz, color='orange', s=150, zorder=5)
ax.text(p_after_rz[0] - 0.3, p_after_rz[1] + 0.3, p_after_rz[2] + 0.4,
        f"p' = [{p_after_rz[0]:.0f}, {p_after_rz[1]:.0f}, {p_after_rz[2]:.0f}]\n(after Rz(pi/2))",
        fontsize=10, color='orange', fontweight='bold')
ax.quiver(0, 0, 0, p_after_rz[0], p_after_rz[1], p_after_rz[2],
          color='orange', arrow_length_ratio=0.04, linewidth=2, alpha=0.6)

# --- Point q (after Ry(-pi/4)) ---
ax.scatter(*q, color='cyan', s=150, zorder=5, edgecolors='darkcyan', linewidths=1.5)
ax.text(q[0] - 0.3, q[1] + 0.4, q[2] - 0.6,
        f"q = [{q[0]:.2f}, {q[1]:.2f}, {q[2]:.2f}]\n(after Ry(-pi/4))",
        fontsize=10, color='darkcyan', fontweight='bold')
ax.quiver(0, 0, 0, q[0], q[1], q[2],
          color='darkcyan', arrow_length_ratio=0.04, linewidth=2, alpha=0.6)

# --- Dashed arcs showing rotation paths ---
# Arc from p to p' (rotation about z-axis, z stays constant at z=2)
t_arc1 = np.linspace(0, -np.pi / 2, 40)
r1 = np.linalg.norm(p[:2])  # radius in xy-plane
angle_start1 = np.arctan2(p[1], p[0])
arc1_x = r1 * np.cos(angle_start1 + t_arc1)
arc1_y = r1 * np.sin(angle_start1 + t_arc1)
arc1_z = np.full_like(t_arc1, p[2])
ax.plot(arc1_x, arc1_y, arc1_z, '--', color='orange', linewidth=2, alpha=0.7)
mid1 = len(t_arc1) // 2
ax.text(arc1_x[mid1] - 1.0, arc1_y[mid1], arc1_z[mid1] + 0.3,
        'Rz(pi/2)', fontsize=9, color='orange', fontstyle='italic')

# Arc from p' to q (rotation about y-axis, y stays constant at y=2)
r2 = np.sqrt(p_after_rz[0]**2 + p_after_rz[2]**2)  # radius in xz-plane
angle_start2 = np.arctan2(p_after_rz[2], p_after_rz[0])
t_arc2 = np.linspace(0, theta_y, 40)
arc2_x = r2 * np.cos(angle_start2 + t_arc2)
arc2_y = np.full_like(t_arc2, p_after_rz[1])
arc2_z = r2 * np.sin(angle_start2 + t_arc2)
ax.plot(arc2_x, arc2_y, arc2_z, '--', color='darkcyan', linewidth=2, alpha=0.7)
mid2 = len(t_arc2) // 2
ax.text(arc2_x[mid2] - 0.3, arc2_y[mid2] + 0.4, arc2_z[mid2],
        'Ry(-pi/4)', fontsize=9, color='darkcyan', fontstyle='italic')

# --- Projection lines for original point ---
ax.plot([p[0], p[0]], [p[1], p[1]], [0, p[2]], 'k--', alpha=0.15)
ax.plot([0, p[0]], [0, p[1]], [0, 0], 'k--', alpha=0.15)

# --- Origin ---
ax.scatter(0, 0, 0, color='black', s=80, zorder=5)
ax.text(0.2, 0.2, 0.2, 'O', fontsize=12, fontweight='bold')

# --- Formatting ---
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Z', fontsize=12)
lim = 6
ax.set_xlim([-lim, lim])
ax.set_ylim([-lim, lim])
ax.set_zlim([-lim, lim])
ax.legend(loc='upper left', fontsize=10)
ax.set_title('Left-click + drag to rotate | Right-click + drag to zoom', fontsize=10, color='gray')

plt.tight_layout()
plt.show()
