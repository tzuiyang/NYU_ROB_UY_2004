# Question 1e: Commutativity of Rotation Matrices — Detailed Explanation

## Background: What Does "Commutative" Mean?

Two operations **commute** if the order you do them in doesn't matter.

For example, with regular numbers, multiplication is commutative:

```
3 x 5 = 5 x 3 = 15
```

But for matrices, multiplication is **generally NOT commutative**:

```
A * B  !=  B * A    (in general)
```

So the question is: **under what special conditions DO rotation matrices commute?**

---

## Key Concept: What Is a Rotation Matrix?

A 3D rotation matrix is a 3x3 matrix that rotates a point around one of the coordinate axes (x, y, or z) by some angle.

For example, rotating by angle theta around the **z-axis**:

```
Rz(theta) = [ cos(theta)  -sin(theta)   0 ]
            [ sin(theta)   cos(theta)   0 ]
            [     0             0        1 ]
```

Notice the bottom-right `1` — this means the **z-component stays the same**. The rotation only mixes x and y. Think of it like spinning a plate on a table — the height (z) doesn't change, only the x-y position rotates.

Similarly:

- **Rx(theta)** rotates around the x-axis (x stays the same, y and z get mixed)
- **Ry(theta)** rotates around the y-axis (y stays the same, x and z get mixed)

---

## Part (a): Rz1 * Rz2 = Rz2 * Rz1 — Is This Necessarily True?

### Answer: YES, this is necessarily true.

### Why?

Both Rz1 and Rz2 rotate around the **same axis** (the z-axis), just by different angles (call them theta1 and theta2).

**Intuition:** Imagine you're standing and spinning around on the spot (rotating around z). If you:

1. Spin 30 degrees, then spin 60 degrees

...you end up in the same place as if you:

1. Spin 60 degrees, then spin 30 degrees

Either way, you've spun a total of 90 degrees. The order doesn't matter because you're always spinning around the **same axis**.

**Mathematical proof:**

When you multiply two z-rotation matrices, you get:

```
Rz(theta1) * Rz(theta2) = Rz(theta1 + theta2)
```

This is because of the trig addition formulas:

```
cos(a)cos(b) - sin(a)sin(b) = cos(a + b)
sin(a)cos(b) + cos(a)sin(b) = sin(a + b)
```

So:

```
Rz(theta1) * Rz(theta2) = Rz(theta1 + theta2)
                         = Rz(theta2 + theta1)     (because addition is commutative)
                         = Rz(theta2) * Rz(theta1)
```

**The key insight:** Two rotations about the SAME axis always combine into a single rotation about that axis by the sum of the angles. Since addition of angles is commutative, the order doesn't matter.

This applies to any pair of rotations about the same axis — two x-rotations commute, two y-rotations commute, two z-rotations commute.

---

## Part (b): Rx * Rz2 = Rz2 * Rx — Is This Necessarily True?

### Answer: NO, this is NOT necessarily true.

### Why?

Rx and Rz2 rotate around **different axes** (x-axis and z-axis). Rotations about different axes generally do NOT commute.

**Intuition:** Grab a book and try this:

**Experiment 1 — Rotate around Z first, then X:**
1. Lay the book flat on a table, cover facing up
2. Rotate it 90 degrees around the z-axis (spin it on the table like a top)
3. Now rotate it 90 degrees around the x-axis (tilt it toward you)
4. Note the book's final position

**Experiment 2 — Rotate around X first, then Z:**
1. Start with the book in the same initial position
2. Rotate it 90 degrees around the x-axis (tilt it toward you first)
3. Now rotate it 90 degrees around the z-axis (spin it on the table)
4. Note the book's final position

**The book ends up in a DIFFERENT orientation!** The order matters.

**Numerical example to prove it:**

Let theta_x = pi/4 (45 degrees) and theta_z = pi/6 (30 degrees):

```
Rx(pi/4) * Rz(pi/6) =  [ 0.866  -0.500   0.000 ]
                        [ 0.354   0.612  -0.707 ]
                        [ 0.354   0.612   0.707 ]

Rz(pi/6) * Rx(pi/4) =  [ 0.866  -0.354   0.354 ]
                        [ 0.500   0.612  -0.612 ]
                        [ 0.000   0.707   0.707 ]
```

These are clearly **different matrices**, which means the rotations give different results.

The word **"necessarily"** is important here. There are special cases where Rx and Rz might happen to commute (for example, when one of the angles is 0, making that rotation the identity matrix — doing nothing). But it is **not guaranteed** for all angles. Since the question asks if it's *necessarily* true (i.e., true for ALL possible angles), the answer is no.

---

## Summary Table

| Statement | Same Axis? | Commutative? | Reason |
|-----------|-----------|-------------|--------|
| Rz1 * Rz2 = Rz2 * Rz1 | Yes (both z) | Always | Angles just add: theta1 + theta2 = theta2 + theta1 |
| Rx * Rz2 = Rz2 * Rx | No (x and z) | Not in general | Different axes produce different results depending on order |

---

## General Rule to Remember

> **Rotations about the SAME axis always commute.**
> **Rotations about DIFFERENT axes generally do NOT commute.**

This is one of the most fundamental properties of 3D rotations and is the reason why describing 3D orientation is much more complex than 2D. In 2D, there is only one axis of rotation (the z-axis, pointing out of the plane), so all 2D rotations commute. In 3D, having multiple axes makes the order of rotations matter, which is why robotics uses tools like rotation matrices, Euler angles, and quaternions to carefully track orientation.
