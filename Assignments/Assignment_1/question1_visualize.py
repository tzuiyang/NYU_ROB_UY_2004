import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ============================================================
# Question 1a & 1b: 2D coordinate frame with p and q
# ============================================================
fig1, ax1 = plt.subplots(1, 1, figsize=(8, 8))
fig1.suptitle("Question 1a & 1b: 2D Coordinate Frame", fontsize=14, fontweight='bold')

# Draw axes
ax1.axhline(0, color='k', linewidth=0.8)
ax1.axvline(0, color='k', linewidth=0.8)
ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('y', fontsize=12)
ax1.set_xlim(-6, 6)
ax1.set_ylim(-6, 6)
ax1.set_aspect('equal')
ax1.grid(True, alpha=0.3)

# Point p = [2, 4]
p = np.array([2, 4])
ax1.plot(p[0], p[1], 'bo', markersize=10)
ax1.annotate(f'p = [{p[0]}, {p[1]}]', xy=(p[0], p[1]),
             xytext=(p[0]+0.3, p[1]+0.3), fontsize=11, color='blue')
ax1.arrow(0, 0, p[0]*0.95, p[1]*0.95, head_width=0.15, head_length=0.1,
          fc='blue', ec='blue', alpha=0.5)

# Rotate p by -pi/2 to get q
theta = -np.pi / 2
R = np.array([[np.cos(theta), -np.sin(theta)],
              [np.sin(theta),  np.cos(theta)]])
q = R @ p  # q = [4, -2]
ax1.plot(q[0], q[1], 'ro', markersize=10)
ax1.annotate(f'q = [{q[0]:.0f}, {q[1]:.0f}]', xy=(q[0], q[1]),
             xytext=(q[0]+0.3, q[1]-0.5), fontsize=11, color='red')
ax1.arrow(0, 0, q[0]*0.95, q[1]*0.95, head_width=0.15, head_length=0.1,
          fc='red', ec='red', alpha=0.5)

# Draw rotation arc from p to q
angle_p = np.degrees(np.arctan2(p[1], p[0]))
angle_q = np.degrees(np.arctan2(q[1], q[0]))
arc_angles = np.linspace(np.radians(angle_p), np.radians(angle_q), 50)
r_arc = 1.5
ax1.plot(r_arc * np.cos(arc_angles), r_arc * np.sin(arc_angles), 'g--', linewidth=1.5)
ax1.annotate(r'$-\pi/2$', xy=(1.5, -0.3), fontsize=11, color='green')

ax1.set_title(f'(a) p = [2, 4]   (b) q = R(-π/2) · p = [{q[0]:.0f}, {q[1]:.0f}]', fontsize=11)

plt.tight_layout()
plt.savefig('q1ab_2d_frame.png', dpi=150, bbox_inches='tight')

# ============================================================
# Question 1c: 3D coordinate frame with p = [2, 4, 2]
# ============================================================
fig2 = plt.figure(figsize=(9, 8))
ax2 = fig2.add_subplot(111, projection='3d')
fig2.suptitle("Question 1c: 3D Coordinate Frame", fontsize=14, fontweight='bold')

p3 = np.array([2, 4, 2])

# Draw coordinate axes
axis_len = 5
ax2.quiver(0, 0, 0, axis_len, 0, 0, color='r', arrow_length_ratio=0.08, linewidth=2, label='x-axis')
ax2.quiver(0, 0, 0, 0, axis_len, 0, color='g', arrow_length_ratio=0.08, linewidth=2, label='y-axis')
ax2.quiver(0, 0, 0, 0, 0, axis_len, color='b', arrow_length_ratio=0.08, linewidth=2, label='z-axis')
ax2.text(axis_len+0.2, 0, 0, 'x', fontsize=13, color='r')
ax2.text(0, axis_len+0.2, 0, 'y', fontsize=13, color='g')
ax2.text(0, 0, axis_len+0.2, 'z', fontsize=13, color='b')

# Plot point p
ax2.scatter(*p3, color='purple', s=100, zorder=5)
ax2.text(p3[0]+0.2, p3[1]+0.2, p3[2]+0.2, f'p = [{p3[0]}, {p3[1]}, {p3[2]}]',
         fontsize=11, color='purple')

# Dashed projection lines
ax2.plot([p3[0], p3[0]], [p3[1], p3[1]], [0, p3[2]], 'k--', alpha=0.3)
ax2.plot([p3[0], p3[0]], [0, p3[1]], [0, 0], 'k--', alpha=0.3)
ax2.plot([0, p3[0]], [p3[1], p3[1]], [0, 0], 'k--', alpha=0.3)
ax2.plot([p3[0], p3[0]], [p3[1], p3[1]], [0, 0], 'k--', alpha=0.3)
ax2.plot([0, p3[0]], [0, 0], [0, 0], 'k--', alpha=0.3)
ax2.plot([0, 0], [0, p3[1]], [0, 0], 'k--', alpha=0.3)

ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_zlabel('z')
ax2.set_title(f'p = [2, 4, 2] in 3D frame', fontsize=11)
ax2.legend(loc='upper left')

plt.tight_layout()
plt.savefig('q1c_3d_frame.png', dpi=150, bbox_inches='tight')

# ============================================================
# Question 1d: Combined rotation matrix (pi/2 about z, then -pi/4 about y)
# ============================================================
fig3, ax3 = plt.subplots(1, 1, figsize=(10, 8))
fig3.suptitle("Question 1d: Combined Rotation Matrix", fontsize=14, fontweight='bold')
ax3.axis('off')

# Compute Rz(pi/2)
theta_z = np.pi / 2
cz, sz = np.cos(theta_z), np.sin(theta_z)
Rz = np.array([[cz, -sz, 0],
               [sz,  cz, 0],
               [0,   0,  1]])

# Compute Ry(-pi/4)
theta_y = -np.pi / 4
cy, sy = np.cos(theta_y), np.sin(theta_y)
Ry = np.array([[cy,  0, sy],
               [0,   1, 0],
               [-sy, 0, cy]])

# Combined: R = Ry(-pi/4) * Rz(pi/2)  (second rotation left-multiplies)
R_combined = Ry @ Rz

s2 = np.sqrt(2)/2

text_lines = []
text_lines.append("Rotate first by pi/2 about z-axis, then by -pi/4 about y-axis:")
text_lines.append("")
text_lines.append("Rz(pi/2) =  [ 0  -1   0 ]")
text_lines.append("            [ 1   0   0 ]")
text_lines.append("            [ 0   0   1 ]")
text_lines.append("")
text_lines.append(f"Ry(-pi/4) = [ {cy:7.4f}   {0:7.4f}   {sy:7.4f} ]")
text_lines.append(f"            [ {0:7.4f}   {1:7.4f}   {0:7.4f} ]")
text_lines.append(f"            [{-sy:7.4f}   {0:7.4f}   {cy:7.4f} ]")
text_lines.append("")
text_lines.append("R = Ry(-pi/4) * Rz(pi/2)")
text_lines.append("")
text_lines.append(f"R = [{R_combined[0,0]:8.4f}  {R_combined[0,1]:8.4f}  {R_combined[0,2]:8.4f} ]")
text_lines.append(f"    [{R_combined[1,0]:8.4f}  {R_combined[1,1]:8.4f}  {R_combined[1,2]:8.4f} ]")
text_lines.append(f"    [{R_combined[2,0]:8.4f}  {R_combined[2,1]:8.4f}  {R_combined[2,2]:8.4f} ]")
text_lines.append("")
text_lines.append("In exact form:")
text_lines.append("R = [    0     -sqrt(2)/2   -sqrt(2)/2 ]")
text_lines.append("    [    1          0             0     ]")
text_lines.append("    [    0     -sqrt(2)/2    sqrt(2)/2  ]")

# Verify with p = [2, 4, 2]
q_d = R_combined @ p3
text_lines.append("")
text_lines.append(f"Verification: R * [2, 4, 2]^T = [{q_d[0]:.4f}, {q_d[1]:.4f}, {q_d[2]:.4f}]^T")

full_text = "\n".join(text_lines)
ax3.text(0.05, 0.95, full_text, transform=ax3.transAxes,
         fontsize=12, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.savefig('q1d_rotation_matrix.png', dpi=150, bbox_inches='tight')

# ============================================================
# Question 1e: Commutativity of rotation matrices
# ============================================================
fig4, ax4 = plt.subplots(1, 1, figsize=(10, 7))
fig4.suptitle("Question 1e: Commutativity of Rotation Matrices", fontsize=14, fontweight='bold')
ax4.axis('off')

# Use sample angles to demonstrate
theta1, theta2, theta_x = np.pi/3, np.pi/6, np.pi/4

c1, s1 = np.cos(theta1), np.sin(theta1)
Rz1 = np.array([[c1, -s1, 0], [s1, c1, 0], [0, 0, 1]])

c2, s2 = np.cos(theta2), np.sin(theta2)
Rz2 = np.array([[c2, -s2, 0], [s2, c2, 0], [0, 0, 1]])

cx, sx = np.cos(theta_x), np.sin(theta_x)
Rx1 = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])

# Check commutativity
product_a1 = Rz1 @ Rz2
product_a2 = Rz2 @ Rz1
commute_a = np.allclose(product_a1, product_a2)

product_b1 = Rx1 @ Rz2
product_b2 = Rz2 @ Rx1
commute_b = np.allclose(product_b1, product_b2)

text_e = []
text_e.append("Given: Rz1, Rz2 rotate about z-axis; Rx1 rotates about x-axis.\n")
text_e.append("─" * 60)

text_e.append("\n(a)  Rz1 · Rz2  =?  Rz2 · Rz1\n")
text_e.append("Rotations about the SAME axis always commute.")
text_e.append("Rz1·Rz2 = Rz(θ1+θ2) = Rz(θ2+θ1) = Rz2·Rz1")
text_e.append(f"\nNumerical check (θ1=π/3, θ2=π/6): Equal? {commute_a}")
text_e.append(f"  → NECESSARILY TRUE ✓\n")

text_e.append("─" * 60)

text_e.append("\n(b)  Rx · Rz2  =?  Rz2 · Rx\n")
text_e.append("Rotations about DIFFERENT axes do NOT generally commute.")
text_e.append(f"\nNumerical check (θx=π/4, θ2=π/6): Equal? {commute_b}")
text_e.append(f"\nRx·Rz2 =\n{np.array2string(product_b1, precision=4, suppress_small=True)}")
text_e.append(f"\nRz2·Rx =\n{np.array2string(product_b2, precision=4, suppress_small=True)}")
text_e.append(f"\n  → NOT NECESSARILY TRUE ✗")

full_text_e = "\n".join(text_e)
ax4.text(0.05, 0.95, full_text_e, transform=ax4.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.savefig('q1e_commutativity.png', dpi=150, bbox_inches='tight')

# ============================================================
# Show all figures
# ============================================================
print("\nAll figures saved as PNG files in the current directory.")
print("  q1ab_2d_frame.png")
print("  q1c_3d_frame.png")
print("  q1d_rotation_matrix.png")
print("  q1e_commutativity.png")
