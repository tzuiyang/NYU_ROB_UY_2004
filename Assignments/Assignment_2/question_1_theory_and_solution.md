# Assignment 2 — Question 1: Homogeneous Transformation Matrices
## Theory, Derivations, and Complete Solutions

---

## Table of Contents

1. [Background Theory](#1-background-theory)
   - [1.1 Coordinate Frames](#11-coordinate-frames)
   - [1.2 Rotation Matrices](#12-rotation-matrices)
   - [1.3 Homogeneous Transformation Matrices](#13-homogeneous-transformation-matrices)
   - [1.4 The Space Frame vs Body Frame Convention](#14-the-space-frame-vs-body-frame-convention-the-most-critical-concept)
   - [1.5 Composing Transformations](#15-composing-transformations)
2. [Part (a) Solution](#2-part-a---translation-in-space-frame-then-rotation-about-space-axis)
3. [Part (b) Solution](#3-part-b---translations-in-body-frame-and-rotation-about-space-axis)
4. [Part (c) Solution](#4-part-c---are-intermediate-frames-unique)
5. [Part (d) Solution](#5-part-d---physical-interpretation-of-t0ee--i)
6. [Summary and Key Takeaways](#6-summary-and-key-takeaways)

---

## 1. Background Theory

### 1.1 Coordinate Frames

A **coordinate frame** (also called a reference frame) is an origin point plus three mutually orthogonal unit vectors (axes). In 3D robotics we use right-hand-rule (RHR) frames: if you curl the fingers of your right hand from x toward y, your thumb points in the z direction.

```
        z
        |
        |
        |_____ y
       /
      /
     x
```

When we write **{S}** we mean the "space" or world frame (fixed, does not move).
When we write **{B}** we mean the "body" frame (attached to a moving link or object).

The transformation matrix **T_SB** answers the question:
*"What is the pose (position + orientation) of frame {B} as measured/expressed in frame {S}?"*

It also lets us convert any point expressed in {B} coordinates into {S} coordinates:

```
p_S = T_SB · p_B
```

---

### 1.2 Rotation Matrices

A rotation matrix R is a 3×3 orthonormal matrix (R^T = R^{-1}, det(R) = +1) that encodes orientation.

#### Rotation about the x-axis by angle θ — Rx(θ)

The x-axis does not move. The y and z axes rotate:

```
        [ 1     0        0    ]
Rx(θ) = [ 0   cos(θ)  -sin(θ) ]
        [ 0   sin(θ)   cos(θ) ]
```

**Memory aid**: x unchanged, (y, z) rotate counterclockwise looking from +x.

**Special values:**
```
Rx(0)    = I             (identity, no rotation)

Rx(π/2)  = [ 1   0   0  ]   (y → z, z → -y)
           [ 0   0  -1  ]
           [ 0   1   0  ]

Rx(π)    = [ 1   0   0  ]   (y → -y, z → -z)
           [ 0  -1   0  ]
           [ 0   0  -1  ]
```

#### Rotation about the y-axis by angle θ — Ry(θ)

```
        [  cos(θ)   0   sin(θ) ]
Ry(θ) = [    0      1     0    ]
        [ -sin(θ)   0   cos(θ) ]
```

**Memory aid**: y unchanged, (z, x) rotate counterclockwise looking from +y.
**Watch out**: The sign pattern is different from Rx and Rz because of the right-hand rule.

#### Rotation about the z-axis by angle θ — Rz(θ)

```
        [ cos(θ)  -sin(θ)   0 ]
Rz(θ) = [ sin(θ)   cos(θ)   0 ]
        [   0         0      1 ]
```

**Memory aid**: z unchanged, (x, y) rotate counterclockwise looking from +z (standard 2D rotation).

**Special values:**
```
Rz(π/4)  = [ √2/2  -√2/2   0 ]   (≈ 0.7071)
           [ √2/2   √2/2   0 ]
           [   0      0    1 ]

Rz(π/2)  = [  0   -1   0 ]
           [  1    0   0 ]
           [  0    0   1 ]

Rz(π)    = [ -1   0   0 ]
           [  0  -1   0 ]
           [  0   0   1 ]
```

#### Key properties of rotation matrices:

- **Orthogonality**: R^T = R^{-1} → R · R^T = I
- **Determinant**: det(R) = +1 (preserves handedness)
- **Composition**: applying R1 then R2 → combined rotation = R2 · R1 (right-to-left order)
- **Non-commutativity**: R1 · R2 ≠ R2 · R1 in general (rotations do NOT commute)

---

### 1.3 Homogeneous Transformation Matrices

A **homogeneous transformation matrix** T is a 4×4 matrix that encodes BOTH rotation AND translation in a single matrix:

```
        [ R   p ]       [ r11  r12  r13  px ]
T_AB =  [       ]  =    [ r21  r22  r23  py ]
        [ 0   1 ]       [ r31  r32  r33  pz ]
                        [  0    0    0    1  ]
```

Where:
- **R** (top-left 3×3): rotation matrix of {B} relative to {A}
- **p** (top-right 3×1 column): position of the origin of {B} expressed in {A}'s coordinates
- **[0 0 0 1]** (bottom row): always this for rigid-body transforms

#### Why homogeneous coordinates?

Without homogeneous coordinates, to transform a point you need BOTH a rotation AND a translation:
```
p_A = R · p_B + p_origin      ← requires two operations
```

With homogeneous coordinates (append 1 to 3D point):
```
[p_A]   [R   p] [p_B]
[    ] = [      ][    ]   ← single matrix multiply does both!
[ 1 ]   [0   1][ 1 ]
```

#### Inverse of a Transformation Matrix

The inverse T^{-1} "reverses" the transformation. For T_AB:
```
            [  R^T   -R^T · p ]
(T_AB)^-1 = [                 ]  = T_BA
            [   0        1    ]
```

**This is very efficient**: instead of computing a full 4×4 inverse, transpose the rotation part and multiply by the negative transposed rotation.

#### Chaining Transformations

If you know {B} in {A} and {C} in {B}:
```
T_AC = T_AB · T_BC
```

This is the fundamental operation in forward kinematics!

---

### 1.4 The Space Frame vs Body Frame Convention (The Most Critical Concept)

This is where most robotics students get confused. When building up a transformation matrix by composing a sequence of primitive operations (pure rotations and pure translations), **the order of matrix multiplication depends on which frame the operation is expressed in**.

#### Definitions

- **Space frame operation**: The primitive transform is expressed relative to the FIXED world frame {S}. These always pre-multiply (go to the LEFT).
- **Body frame operation**: The primitive transform is expressed relative to the CURRENT body frame (which has been modified by previous operations). These always post-multiply (go to the RIGHT).

#### The Rule

```
Space frame (fixed):   T_new = T_primitive · T_current   [pre-multiply / left multiply]
Body frame (current):  T_new = T_current · T_primitive   [post-multiply / right multiply]
```

#### Intuition: Why Does Space Frame Pre-Multiply?

When you operate in the SPACE frame, you're rotating or translating about/along world axes. Those world axes are ALWAYS the same — they don't move. Each new space-frame operation "wraps around" the accumulated transformation from the LEFT.

When you operate in the BODY frame, you're rotating or translating about/along the body's OWN axes (which keep changing as you compose operations). The new operation builds on top of what's already there, so it goes on the RIGHT.

#### Example to Clarify

Suppose we want:
**Step 1**: Rotate 90° about z_S (world/space z-axis)
**Step 2**: Translate 3 units in x_B (the body x-axis, which is NOW pointing in y_S after the rotation!)

```
After Step 1: T = Rz(90°)
After Step 2 (body frame, post-multiply): T = Rz(90°) · Trans(x, 3)
```

The body x-axis after rotating 90° about z now points in the world y-direction.
So translating 3 in body x = translating 3 in world y.

Let's verify: Trans(x, 3) in homogeneous form = [1,0,0,3; 0,1,0,0; 0,0,1,0; 0,0,0,1]

Rz(90°) · Trans(x, 3):
```
[ 0  -1  0  0 ]   [ 1  0  0  3 ]   [ 0  -1  0   0 ]
[ 1   0  0  0 ] × [ 0  1  0  0 ] = [ 1   0  0   3 ]
[ 0   0  1  0 ]   [ 0  0  1  0 ]   [ 0   0  1   0 ]
[ 0   0  0  1 ]   [ 0  0  0  1 ]   [ 0   0  0   1 ]
```

The origin of {B} is at (0, 3, 0) in {S} — which IS 3 units in the world y direction. ✓

If instead we accidentally used space frame (pre-multiply) for the body translation:
Trans(x, 3) · Rz(90°):
```
[ 1  0  0  3 ]   [ 0  -1  0  0 ]   [ 0  -1  0  3 ]
[ 0  1  0  0 ] × [ 1   0  0  0 ] = [ 1   0  0  0 ]
[ 0  0  1  0 ]   [ 0   0  1  0 ]   [ 0   0  1  0 ]
[ 0  0  0  1 ]   [ 0   0  0  1 ]   [ 0   0  0  1 ]
```

The origin of {B} would be at (3, 0, 0) in {S} — which is 3 in world x, NOT body x. Wrong!

#### Summary Table

| Operation described in... | Matrix multiply rule | New operation goes... |
|--------------------------|---------------------|----------------------|
| **Space frame {S}** (world axes) | Pre-multiply | LEFT of current T |
| **Body frame {B}** (body axes) | Post-multiply | RIGHT of current T |

---

### 1.5 Composing Transformations

When you have a sequence of N operations:

```
Starting from identity (T = I):
Apply op1 → T1
Apply op2 → T2
...
Apply opN → TN = T_SB
```

For ALL space-frame operations:
```
T_SB = T_opN · T_op(N-1) · ... · T_op2 · T_op1
```
(rightmost = first applied, leftmost = last applied)

For ALL body-frame operations:
```
T_SB = T_op1 · T_op2 · ... · T_op(N-1) · T_opN
```
(leftmost = first applied, rightmost = last applied)

For MIXED space+body operations: apply the rules individually (pre-multiply for space, post-multiply for body).

---

## 2. Part (a) — Translation in Space Frame, then Rotation about Space Axis

### Problem Statement

> Given two frames {S} and {B}, write out T_SB such that going from {S} to {B} there is:
> 1. A translation of **4 units** in the positive **y_S** direction
> 2. Then a rotation about **z_S** of **π/4** rad

Both operations are expressed in the SPACE frame (note the subscripts: y_S, z_S).

---

### Step 1: Identify the Operations and Their Frame

| # | Operation | Frame | Rule |
|---|-----------|-------|------|
| 1 | Translate 4 in y_S | Space frame | Pre-multiply |
| 2 | Rotate π/4 about z_S | Space frame | Pre-multiply |

---

### Step 2: Write Out the Primitive Matrices

**Translation T1 — 4 units in y_S:**
```
           [ 1   0   0   0 ]
Trans(y,4) = [ 0   1   0   4 ]
           [ 0   0   1   0 ]
           [ 0   0   0   1 ]
```

**Rotation T2 — π/4 about z_S:**

Recall: cos(π/4) = sin(π/4) = √2/2 ≈ 0.7071

```
              [ cos(π/4)  -sin(π/4)   0   0 ]   [ √2/2  -√2/2   0   0 ]
Rot(z, π/4) = [ sin(π/4)   cos(π/4)   0   0 ] = [ √2/2   √2/2   0   0 ]
              [    0           0       1   0 ]   [   0      0    1   0 ]
              [    0           0       0   1 ]   [   0      0    0   1 ]
```

---

### Step 3: Apply the Space-Frame Pre-Multiply Rule

Since BOTH operations are in the space frame:

- **Step 1** (translate in y_S): T = Trans(y, 4)
- **Step 2** (rotate about z_S, space frame → pre-multiply): T_SB = Rot(z, π/4) · Trans(y, 4)

```
T_SB = Rot(z, π/4) · Trans(y, 4)
```

---

### Step 4: Multiply the Matrices

```
         [ √2/2  -√2/2   0   0 ]   [ 1   0   0   0 ]
T_SB =   [ √2/2   √2/2   0   0 ] × [ 0   1   0   4 ]
         [   0      0    1   0 ]   [ 0   0   1   0 ]
         [   0      0    0   1 ]   [ 0   0   0   1 ]
```

The rotation part R stays the same (bottom-left of product):
```
R_SB = Rot(z, π/4) = [ √2/2  -√2/2   0 ]
                     [ √2/2   √2/2   0 ]
                     [   0      0    1 ]
```

The translation column p = Rot(z, π/4) · [0, 4, 0]^T:
```
px = (√2/2)(0) + (-√2/2)(4) + (0)(0) = -4·(√2/2) = -2√2
py = (√2/2)(0) + ( √2/2)(4) + (0)(0) = +4·(√2/2) = +2√2
pz = (0)(0)    + (0)(4)     + (1)(0) = 0
```

---

### Final Answer — Part (a)

```
         [ √2/2  -√2/2   0   -2√2 ]
T_SB =   [ √2/2   √2/2   0   +2√2 ]
         [   0      0    1    0   ]
         [   0      0    0    1   ]
```

In decimal form (√2/2 ≈ 0.7071, 2√2 ≈ 2.8284):

```
         [ 0.7071  -0.7071   0   -2.8284 ]
T_SB ≈   [ 0.7071   0.7071   0   +2.8284 ]
         [   0        0      1     0     ]
         [   0        0      0     1     ]
```

---

### Physical Interpretation of Part (a)

**Rotation part R_SB = Rz(π/4)**: The axes of {B} are rotated 45° counterclockwise from {S} about the z-axis.

**Origin position p = (-2√2, +2√2, 0)**:

The origin of {B} in {S} is NOT at (0, 4, 0). Why?
Because we first translated to (0, 4, 0) and THEN rotated EVERYTHING by 45° about the world z-axis (which passes through the world origin (0,0,0)). This rotation sweeps the point (0, 4, 0) around the z-axis:

```
Original point: (0, 4, 0)
After Rz(π/4):
    x' = 0·cos(45°) - 4·sin(45°) = -2√2  ≈ -2.83
    y' = 0·sin(45°) + 4·cos(45°) = +2√2  ≈ +2.83
    z' = 0
```

**Visualization (top view — xy plane):**

```
   y_S
    |
    |     * (0, 4)  ← where {B}'s origin is BEFORE the rotation about z_S
    |    /
    |   / 45° arc
    |  /
    | /
    |/_________ x_S
   /
  * (-2.83, 2.83)  ← where {B}'s origin ends up AFTER rotating about world z
```

This is why the space-frame convention makes a rotation about z_S "sweep" previously translated points — the z_S axis goes through the WORLD ORIGIN, not through the translated frame's origin.

---

## 3. Part (b) — Translations in Body Frame and Rotation about Space Axis

### Problem Statement

> Given two frames {S} and {B}, write out T_SB such that going from {S} to {B} there is:
> 1. A translation of **7 units** in the positive **y_B** direction
> 2. A translation of **9 units** in the positive **z_B** direction
> 3. A rotation about **x_S** of **π/2** rad

**CRITICAL OBSERVATION**: The translations are in **y_B and z_B (body frame)**, but the rotation is about **x_S (space frame)**. This is a MIXED case.

---

### Step 1: Unpack the Mixed Convention

The translations are given in the BODY frame {B}. But {B}'s orientation isn't defined yet without knowing the rotation. Therefore:
- The rotation R_SB = Rot(x, π/2) defines the orientation of {B} relative to {S} first
- The translations 7 in y_B and 9 in z_B tell us where the origin of {B} is, BUT expressed in the body frame's coordinate directions

To find the origin position in {S}, we must convert body-frame directions to space-frame directions using R_SB.

---

### Step 2: Determine R_SB

```
              [ 1     0        0     ]
Rx(π/2)    =  [ 0   cos(π/2)  -sin(π/2) ]
              [ 0   sin(π/2)   cos(π/2) ]

             = [ 1   0   0 ]
               [ 0   0  -1 ]
               [ 0   1   0 ]
```

cos(π/2) = 0, sin(π/2) = 1

So after rotating by π/2 about x_S:
- x_B aligns with x_S (x unchanged)
- **y_B now points in the z_S direction**   → ŷ_B = [0, 0, 1]^T in {S}
- **z_B now points in the −y_S direction** → ẑ_B = [0, -1, 0]^T in {S}

**Geometric insight:** Rx(π/2) is a 90° rotation about the x-axis. Looking from the +x direction, y rotates into z (y → z) and z rotates into −y (z → −y).

```
Before Rx(π/2):   After Rx(π/2):
   z                   y_B
   |                   ↑
   |                   |
   |___y     →     x_B ___z_B  (but z_B points INTO the page)
                              And z_B → -y direction in space
```

---

### Step 3: Convert Body-Frame Translations to Space Frame

The origin of {B} is described as:
- 7 units along y_B
- 9 units along z_B

In space frame {S}:
```
p_SB = 7 · ŷ_B (in {S}) + 9 · ẑ_B (in {S})
     = 7 · [0, 0, 1]^T  + 9 · [0, -1, 0]^T
     = [0, 0, 7]^T + [0, -9, 0]^T
     = [0, -9, 7]^T
```

Or equivalently using the rotation matrix:
```
p_SB = R_SB · [0, 7, 9]^T = Rx(π/2) · [0, 7, 9]^T

     = [ 1   0   0 ] [0]   [  0  ]
       [ 0   0  -1 ] [7] = [ -9  ]
       [ 0   1   0 ] [9]   [  7  ]
```

So p_SB = (0, -9, 7) in {S} coordinates. ✓

---

### Step 4: Assemble T_SB

```
         [ R_SB  |  p_SB ]
T_SB =   [               ]
         [  0    |    1   ]

       = [ 1   0   0  |   0 ]
         [ 0   0  -1  |  -9 ]
         [ 0   1   0  |   7 ]
         [ 0   0   0  |   1 ]
```

---

### Alternative Derivation: Matrix Multiplication

We can also derive this using the mixed space/body convention directly:

**Order**: Rotation about x_S (space frame, pre-multiply), then translations in body frame (post-multiply):

```
T_SB = Rot(x_S, π/2) · Trans(y_B, 7) · Trans(z_B, 9)
     = Rot(x_S, π/2) · Trans([0, 7, 9])
```

(The two body-frame translations combine simply since pure translations commute)

```
         [ 1   0   0   0 ]   [ 1   0   0   0 ]
T_SB =   [ 0   0  -1   0 ] × [ 0   1   0   7 ]
         [ 0   1   0   0 ]   [ 0   0   1   9 ]
         [ 0   0   0   1 ]   [ 0   0   0   1 ]
```

Translation column = Rot(x, π/2) · [0, 7, 9]^T = [0, -9, 7]^T (same as above ✓)

---

### Final Answer — Part (b)

```
         [ 1   0   0    0 ]
T_SB =   [ 0   0  -1   -9 ]
         [ 0   1   0    7 ]
         [ 0   0   0    1 ]
```

---

### Physical Interpretation of Part (b)

**Rotation part R_SB = Rx(π/2)**: The frame {B} is tilted 90° about the x-axis. What was the y-axis of {B} now points "up" (z_S direction), and what was the z-axis of {B} now points "down" (−y_S direction).

**Origin position p = (0, −9, 7)**:

The origin of {B} in {S} is 9 units in the NEGATIVE y_S direction and 7 units in the POSITIVE z_S direction. This is exactly what "7 in body y" and "9 in body z" means AFTER rotating the body 90° about x — because the body y is the space z, and the body z is the negative space y.

---

## 4. Part (c) — Are Intermediate Frames Unique?

### Problem Statement

> Two engineers each design a coordinate frame system for a 4 DOF robot arm. Both arrive at the same final T_0EE(θ₁, θ₂, θ₃, θ₄). Will engineer A's T_01 necessarily be identical to engineer B's T_01?

### Answer: NO — Not Necessarily

The intermediate frames are **design choices**, not uniquely determined by the physics of the robot.

### Why Not?

The forward kinematics chain is:
```
T_0EE = T_01 · T_12 · T_23 · T_3EE
```

This is a product of four matrices. There are **infinitely many ways** to decompose a single 4×4 transformation matrix into a product of simpler matrices. Even if the TOTAL product T_0EE is the same, the individual factors can be completely different.

### Concrete Example

Consider a simple 2D case: a matrix M = A · B · C can also be written as M = A' · B' · C' where:
- A' = A · D
- B' = D^{-1} · B · E
- C' = E^{-1} · C

for any invertible D and E. The product is the same: A' · B' · C' = A · D · D^{-1} · B · E · E^{-1} · C = A · B · C = M.

### In Practice: Why Do Frame Assignments Differ?

When designing a multi-link robot, each engineer must choose where to place frame {1} (attached to link 1), frame {2} (attached to link 2), etc. Common but different valid choices include:

| Choice | Engineer A might say... | Engineer B might say... |
|--------|------------------------|------------------------|
| Frame {1} origin | At joint 1 | At center of mass of link 1 |
| Frame {1} z-axis direction | Along the joint 1 rotation axis (upward) | Along the joint 1 rotation axis (downward) |
| Frame {2} x-axis | Pointing toward joint 3 | Pointing toward joint 2 |
| DH parameter assignment | Standard DH | Modified DH |

Both engineers can construct a valid kinematic model that gives the SAME T_0EE for all configurations, but every intermediate T_i{i+1} can be completely different.

### Formal Statement

The decomposition of T_0EE into individual T_i{i+1} factors is **not unique**. The intermediate frames are **design variables**. In particular, the Denavit-Hartenberg (DH) convention is a systematic way to choose frames, but different engineers may make different DH assignments and still get the same final FK.

**Answer: No, T_01 does NOT have to be the same. The individual intermediate transforms are not uniquely determined by the final T_0EE.**

---

## 5. Part (d) — Physical Interpretation of T_0EE = I

### Problem Statement

> A 5 DOF robotic arm with reach 1.2m has:
> T_0EE(θ₁,θ₂,θ₃,θ₄,θ₅) = T_01(θ₁) · T_12(θ₂) · T_23(θ₃) · T_34(θ₄) · T_45(θ₅) · T_5EE()
>
> What is the physical interpretation of T_0EE = I for a specific set of joint angles?

### The Identity Matrix

The 4×4 identity matrix is:
```
    [ 1   0   0   0 ]
I = [ 0   1   0   0 ]
    [ 0   0   1   0 ]
    [ 0   0   0   1 ]
```

Reading the structure of a transformation matrix:
```
        [ R   p ]
T_0EE = [       ]  where R = top-left 3×3, p = top-right 3×1
        [ 0   1 ]
```

Setting T_0EE = I means:
- **R = I₃ₓ₃** (the 3×3 identity rotation)
- **p = [0, 0, 0]^T** (zero translation vector)

### Physical Interpretation

**T_0EE = I means the end-effector frame {EE} coincides exactly with the base frame {0}.**

More specifically, this simultaneously means:

#### 1. Zero Translation: p = [0, 0, 0]^T

The origin of the end-effector frame {EE} is at the **exact same location** as the origin of the base frame {0}. The tip of the robot arm is at position (0, 0, 0) relative to the base.

#### 2. Zero Rotation: R = I

The orientation of {EE} is **identical** to the orientation of {0}. All axes of the end-effector frame are perfectly aligned with the base frame axes:
- x_EE points the same direction as x_0
- y_EE points the same direction as y_0
- z_EE points the same direction as z_0

### Visualization

```
                          ___
                         /   \  End-effector
                         \___/
                          |
Side view of robot:       |  (link 5, 45, etc.)
                          |
        ___              /
       |   |            /  (links folding back on themselves)
       |{0}|<----------/
       |___|
    BASE FRAME
    (also EE frame
     location!)
```

The arm has **folded back on itself** such that the end-effector returns to the exact position AND orientation of the base frame. Every link's contribution to translation and rotation has been perfectly canceled out by the subsequent links.

Imagine you are standing at the origin of the robot base ({0}). For T_0EE = I, if you could look through the end-effector's "eyes," you would see the world with exactly the same orientation as if you were looking from the base frame's axes.

### Is This Physically Possible?

With a 5 DOF arm and reach of 1.2m, **YES — it is possible** that such a configuration exists. Consider:

- The arm must "fold over" so that the tip comes back to the base origin (0, 0, 0).
- Since the reach is 1.2m, the links must sum to zero displacement, which requires them to double back.
- The 5 DOFs must also conspire to make the rotation align perfectly.

**Important nuances:**

1. **It is NOT just "the robot is at rest" or "zero position"** — unless the robot is specifically designed so that the home configuration gives the end-effector at the base origin.

2. **The arm is almost certainly NOT straight** — a straight arm configuration would typically put the EE far away from the base, not at the base.

3. **It is similar to the concept of a "null displacement"** — the total rigid-body transformation is the identity, meaning no net movement from {0} to {EE}.

4. **Analogy**: It is like walking around a city and returning to exactly where you started, facing exactly the same direction. Each joint angle is a "turn" and each link length is a "step," and the configuration T_0EE = I means you have returned exactly home.

### Drawing

```
   z_0 (= z_EE)
    |
    |
    |_____ y_0 (= y_EE)
   /
  x_0 (= x_EE)
   ↑
   Here: {0} and {EE} perfectly overlap

One possible arm configuration achieving this (schematic):

        ___
  /~~~~\   End-effector at origin,
  \    /   same orientation as base
   \  /
    \/  ← joint 5 (θ₅)
    /\  ← joint 4 (θ₄)
   /  \
  /    \
 /      \
◎ ← joint 1 = base origin {0}
```

The arm has looped back so the EE frame overlays the base frame. Like a human arm that has been folded to put the hand back at the shoulder with the same palm orientation.

---

## 6. Summary and Key Takeaways

### Formulas at a Glance

**Rotation matrices:**
```
Rx(θ) = [1, 0, 0; 0, cθ, -sθ; 0, sθ, cθ]
Ry(θ) = [cθ, 0, sθ; 0, 1, 0; -sθ, 0, cθ]
Rz(θ) = [cθ, -sθ, 0; sθ, cθ, 0; 0, 0, 1]
```

**Homogeneous matrix:**
```
T = [R, p; 0, 1]   (R is 3×3 rotation, p is 3×1 position in parent frame)
```

**Key rules:**
```
Space frame op → Pre-multiply  (T_new = T_op · T_current)
Body frame op  → Post-multiply (T_new = T_current · T_op)
```

### Part (a) Answer

Translation of 4 in y_S, then rotation π/4 about z_S (both space frame):

```
T_SB = Rz(π/4) · Trans(y, 4) = [ √2/2  -√2/2   0   -2√2 ]
                                [ √2/2   √2/2   0   +2√2 ]
                                [   0      0    1     0   ]
                                [   0      0    0     1   ]
```

### Part (b) Answer

Rotation π/2 about x_S (space frame); translations 7 in y_B, 9 in z_B (body frame):

```
T_SB = Rx(π/2) · Trans([0,7,9]) = [ 1   0   0    0 ]
                                   [ 0   0  -1   -9 ]
                                   [ 0   1   0    7 ]
                                   [ 0   0   0    1 ]
```

### Part (c) Answer

**No**, engineer A's T_01 is not necessarily identical to engineer B's T_01. Intermediate frame assignments are design choices. As long as the product of all individual transformation matrices yields the same T_0EE, the individual factors can differ.

### Part (d) Answer

T_0EE = I means the end-effector frame {EE} **coincides exactly with the base frame {0}** — same position (origin at (0,0,0)) AND same orientation (all axes aligned). The arm has folded back on itself to return the EE to the base with zero net rotation. This is a "null displacement" configuration.

---

*End of Question 1 Theory and Solutions*
