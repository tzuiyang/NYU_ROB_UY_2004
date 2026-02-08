# Question 1d: Combined Rotation Matrix — Detailed Explanation

## The Problem

We have a point **p = [2, 4, 2]** in 3D space. We want to:

1. **First**, rotate it by **pi/2** (90 degrees) about the **z-axis**
2. **Then**, rotate it by **-pi/4** (-45 degrees) about the **y-axis**

We need to write out the single rotation matrix R that does both of these in one step.

---

## Step 1: Understand Each Rotation Matrix

### Rotation about the z-axis by angle theta

```
Rz(theta) = [ cos(theta)  -sin(theta)   0 ]
            [ sin(theta)   cos(theta)   0 ]
            [     0             0        1 ]
```

This rotates the x and y components while leaving z unchanged. Think of it as spinning a point on a table when you look down from above.

### Rotation about the y-axis by angle theta

```
Ry(theta) = [  cos(theta)   0   sin(theta) ]
            [      0        1       0       ]
            [ -sin(theta)   0   cos(theta)  ]
```

This rotates the x and z components while leaving y unchanged. Think of it as tilting something forward or backward.

---

## Step 2: Plug In the Angles

### Rz(pi/2) — 90 degrees about z

```
cos(pi/2) = 0
sin(pi/2) = 1
```

```
Rz(pi/2) = [ 0  -1   0 ]
           [ 1   0   0 ]
           [ 0   0   1 ]
```

**What does this do?** It swaps x and y (with a sign change). If a point is at (x, y, z), after this rotation it moves to (-y, x, z). For example, a point at (1, 0, 0) on the x-axis moves to (0, 1, 0) on the y-axis — a 90-degree counterclockwise spin when viewed from above.

### Ry(-pi/4) — negative 45 degrees about y

```
cos(-pi/4) = cos(pi/4) = sqrt(2)/2 ≈ 0.7071
sin(-pi/4) = -sin(pi/4) = -sqrt(2)/2 ≈ -0.7071
```

```
Ry(-pi/4) = [  sqrt(2)/2    0   -sqrt(2)/2 ]
            [      0        1        0      ]
            [  sqrt(2)/2    0    sqrt(2)/2  ]
```

**What does this do?** It tilts the point by -45 degrees around the y-axis. The y-component stays the same, while x and z get mixed together. The negative angle means it tilts in the clockwise direction when viewed from the positive y-axis.

---

## Step 3: Combine Into One Matrix

### The Order Rule (CRITICAL!)

When we apply rotations **sequentially**, the **second rotation goes on the LEFT** when we multiply:

```
q = R_second * R_first * p
```

This is because matrix multiplication works right-to-left. The matrix closest to the point p gets applied first.

So if we:
1. First rotate by Rz(pi/2)
2. Then rotate by Ry(-pi/4)

The combined matrix is:

```
R = Ry(-pi/4) * Rz(pi/2)
```

**NOT** Rz * Ry! This is a very common mistake. Always remember: **last rotation applied goes on the left**.

### Why Does the Second Rotation Go on the Left?

Think about it step by step:

```
Step 1:  p'  = Rz * p          (first rotation)
Step 2:  q   = Ry * p'         (second rotation)
```

Substitute step 1 into step 2:

```
q = Ry * (Rz * p) = (Ry * Rz) * p
```

So the combined matrix is R = Ry * Rz, with the second rotation on the left.

---

## Step 4: Do the Matrix Multiplication

```
R = Ry(-pi/4) * Rz(pi/2)

    [ √2/2   0   -√2/2 ]     [ 0  -1   0 ]
  = [  0     1     0    ]  *  [ 1   0   0 ]
    [ √2/2   0    √2/2  ]    [ 0   0   1 ]
```

Multiply row by column:

### Row 1 of Ry * each column of Rz:

```
R[0,0] = (√2/2)(0)  + (0)(1)  + (-√2/2)(0)  = 0
R[0,1] = (√2/2)(-1) + (0)(0)  + (-√2/2)(0)  = -√2/2
R[0,2] = (√2/2)(0)  + (0)(0)  + (-√2/2)(1)  = -√2/2
```

### Row 2 of Ry * each column of Rz:

```
R[1,0] = (0)(0)  + (1)(1)  + (0)(0)  = 1
R[1,1] = (0)(-1) + (1)(0)  + (0)(0)  = 0
R[1,2] = (0)(0)  + (1)(0)  + (0)(1)  = 0
```

### Row 3 of Ry * each column of Rz:

```
R[2,0] = (√2/2)(0)  + (0)(1)  + (√2/2)(0)  = 0
R[2,1] = (√2/2)(-1) + (0)(0)  + (√2/2)(0)  = -√2/2
R[2,2] = (√2/2)(0)  + (0)(0)  + (√2/2)(1)  = √2/2
```

---

## Final Result

```
R = Ry(-pi/4) * Rz(pi/2)

    [    0      -√2/2    -√2/2  ]
R = [    1        0        0    ]
    [    0      -√2/2     √2/2  ]
```

In decimal form (√2/2 ≈ 0.7071):

```
    [  0.0000   -0.7071   -0.7071 ]
R = [  1.0000    0.0000    0.0000 ]
    [  0.0000   -0.7071    0.7071 ]
```

---

## Verification: Apply R to p = [2, 4, 2]

```
q = R * p

q[0] = (0)(2) + (-√2/2)(4) + (-√2/2)(2) = -4√2/2 - 2√2/2 = -6√2/2 = -3√2 ≈ -4.2426
q[1] = (1)(2) + (0)(4)     + (0)(2)      = 2
q[2] = (0)(2) + (-√2/2)(4) + (√2/2)(2)   = -4√2/2 + 2√2/2 = -2√2/2 = -√2  ≈ -1.4142
```

So:

```
q = [-3√2, 2, -√2] ≈ [-4.2426, 2.0000, -1.4142]
```

We can double-check by doing the rotations one at a time:

```
Step 1: Rz(pi/2) * [2, 4, 2] = [-4, 2, 2]     (x and y swap with sign change)
Step 2: Ry(-pi/4) * [-4, 2, 2] = [-4.2426, 2, -1.4142]    (x and z mix)
```

Both approaches give the same answer, confirming our combined matrix is correct.

---

## Step-by-Step Calculation: Rotating p = [2, 4, 2]

Let's walk through the full arithmetic for each rotation individually.

### Rotation 1: Rz(pi/2) * p — Spin 90 degrees about z

```
p' = Rz(pi/2) * p

     [ 0  -1   0 ]     [ 2 ]
p' = [ 1   0   0 ]  *  [ 4 ]
     [ 0   0   1 ]     [ 2 ]
```

Multiply each row by the column vector p:

```
p'[0] = (0)(2) + (-1)(4) + (0)(2)  =  0 - 4 + 0  =  -4
p'[1] = (1)(2) + (0)(4)  + (0)(2)  =  2 + 0 + 0  =   2
p'[2] = (0)(2) + (0)(4)  + (1)(2)  =  0 + 0 + 2  =   2
```

```
p' = [-4, 2, 2]
```

**What happened geometrically?**
- The z-component stayed at 2 (rotation about z doesn't change z)
- The original (x, y) = (2, 4) became (-4, 2)
- This is the standard 90-degree CCW rotation in the xy-plane: (x, y) → (-y, x)

You can verify: (-y, x) = (-4, 2) ✓

### Rotation 2: Ry(-pi/4) * p' — Tilt -45 degrees about y

```
q = Ry(-pi/4) * p'

     [  √2/2    0   -√2/2 ]     [ -4 ]
q  = [   0      1     0   ]  *  [  2 ]
     [  √2/2    0    √2/2 ]     [  2 ]
```

where √2/2 ≈ 0.7071.

Multiply each row by the column vector p':

```
q[0] = (√2/2)(-4) + (0)(2) + (-√2/2)(2)
     = -4√2/2 + 0 - 2√2/2
     = -4(0.7071) - 2(0.7071)
     = -2.8284 - 1.4142
     = -4.2426
     = -3√2     (exact)

q[1] = (0)(-4) + (1)(2) + (0)(2)
     = 0 + 2 + 0
     = 2

q[2] = (√2/2)(-4) + (0)(2) + (√2/2)(2)
     = -4√2/2 + 0 + 2√2/2
     = -4(0.7071) + 2(0.7071)
     = -2.8284 + 1.4142
     = -1.4142
     = -√2     (exact)
```

```
q = [-3√2, 2, -√2] ≈ [-4.2426, 2.0000, -1.4142]
```

**What happened geometrically?**
- The y-component stayed at 2 (rotation about y doesn't change y)
- The (x, z) = (-4, 2) got mixed together by a -45 degree rotation
- The point moved in the xz-plane while keeping its distance from the y-axis

### Summary of the Journey

```
                  Rz(pi/2)                    Ry(-pi/4)
p = [2, 4, 2]  ──────────►  p' = [-4, 2, 2]  ──────────►  q = [-4.24, 2.00, -1.41]
  (original)              (after z-rotation)             (after y-rotation)
```

| Point | x | y | z | What changed |
|-------|------|------|------|-------------|
| p (original) | 2 | 4 | 2 | Starting point |
| p' (after Rz) | -4 | 2 | 2 | x,y rotated 90° CCW; z unchanged |
| q (after Ry) | -4.24 | 2 | -1.41 | x,z rotated -45°; y unchanged |

Notice the pattern: each rotation only mixes two of the three coordinates, leaving the axis of rotation's component untouched.

---

## Key Takeaways

1. **Build each rotation matrix** by plugging the angle into the standard formula for that axis
2. **Combine by multiplying** with the second (later) rotation on the LEFT: R = R_second * R_first
3. **The "left multiply" rule** comes from substitution: q = R2 * (R1 * p) = (R2 * R1) * p
4. **Verify your answer** by applying the combined matrix to a test point and comparing with doing the rotations one at a time
