import numpy as np

# q2 part a
def rotate2D(theta, p_point):
    R = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]])
    q_point = np.matmul(R, p_point)
    return q_point

# q2 part b
def rotate3D(theta, axis_of_rotation, p_point):
    c = np.cos(theta)
    s = np.sin(theta)

    if axis_of_rotation == 'z':
        R = np.array([[ c, -s,  0],
                      [ s,  c,  0],
                      [ 0,  0,  1]])
    elif axis_of_rotation == 'y':
        R = np.array([[ c,  0,  s],
                      [ 0,  1,  0],
                      [-s,  0,  c]])
    elif axis_of_rotation == 'x':
        R = np.array([[ 1,  0,  0],
                      [ 0,  c, -s],
                      [ 0,  s,  c]])

    q_point = np.matmul(R, p_point)
    return q_point

# q2 part c
def rotate3D_many_times(rotation_list, p_point):
    q_point = p_point
    for rotation in rotation_list:
        theta = rotation[0]
        axis = rotation[1]
        q_point = rotate3D(theta, axis, q_point)
    return q_point