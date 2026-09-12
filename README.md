# Lab 4: Follow the Gap

## I. Learning Goals

- Reactive methods for obstacle avoidance

## II. Overview

In this lab, you will implement a reactive algorithm for obstacle avoidance. While the base starter code defines an implementation of the F1TENTH Follow the Gap Algorithm, you are allowed to submit in C++, and encouraged to try different reactive algorithms or a combination of several. In total, the python code for the algorithm is only about 120 lines.

## III. Review of F1TENTH Follow the Gap

The lecture slides on F1TENTH Follow the gap is the best visual resource for understanding every step of the algorithm. However, the steps are outlined over here:

1. Obtain laser scans and preprocess them.
2. Find the closest point in the LiDAR ranges array.
3. Draw a safety bubble around this closest point and set all points inside this bubble to 0. All other non-zero points are now considered “gaps” or “free space”.
4. Find the max length “gap”, in other words, the largest number of consecutive non-zero elements in your ranges array.
5. Find the best goal point in this gap. Naively, this could be the furthest point away in your gap, but you can probably go faster if you follow the “Better Idea” method as described in lecture.
6. Actuate the car to move towards this goal point by publishing an `AckermannDriveStamped` to the /drive topic.

### IV. Implementation

Implement a gap follow algorithm to make the car drive autonomously around the Levine Hall map. You can implement this node in either C++ or Python.

Test in the [f1tenth_gym_ros](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-jazzy) simulator on two of its maps: `levine_blocked`, the empty Levine loop with its doorways sealed, and `levine_obs`, the loop with its corner doorways bricked up and thirteen obstacles added (a slalom of boxes and an ellipse on the south hallway, two triangles and a box on the north hallway) that are relatively hard to navigate through. Pick one with `map_path: 'maps/levine_blocked'` or `map_path: 'maps/levine_obs'` in `config/sim.yaml`. Both come with a centerline, so the simulator counts your laps (`/ego_racecar/lap_count`, and a "completed lap" line in the bridge log). The autograder drives your node on the same two maps: `levine_blocked` counter-clockwise from the south hallway just behind the finish line, heading east; `levine_obs` counter-clockwise too, from the east hallway just past its south corner (`sx: 9.96, sy: 2.8, stheta: 1.5708` in `config/sim.yaml`), heading north, so the north-hallway obstacles and three corners come first and only a full lap has to thread the south-hallway slalom. Test both directions: an obstacle that is easy from one side can be a trap from the other (the L-shaped wall on the north hallway is a dead-end pocket with the way through above it).

Your node must subscribe to `/scan` and publish `AckermannDriveStamped` on `/drive`, and it must work when started with a plain `ros2 run gap_follow <executable>`: the autograder passes no parameter file, so bake your tuned bubble size, thresholds and speeds into the node's defaults. Tip: a gap is only worth aiming at if the car fits through it; the closest-point bubble alone does not tell you that.

### V. Deliverables and Submission

**Deliverable 1**: After you're finished, update the entire skeleton package directory with your `gap_follow` package and directly commit and push to the repo Classroom 50 created for you. Your committed code should start and run in simulation smoothly, this includes building as a package with any dependencies included as part of the ``package.xml``. The basic requirement is that your car should be able to navigate entire loops in the `levine_blocked` map, and through at least 3 corners of the `levine_obs` map. You get 5 bonus points if your implementation is able to complete all 4 corners and keeps lapping through the map. The autograder watches both runs in the simulator, so no screencast is needed for them.

**Deliverable 2**: Take a video of the algorithm running on the real car. Upload it to YouTube (unlisted) or Google Drive — for Drive, set sharing to **"Anyone with the link can view"** or we cannot grade it — and include the link in **`SUBMISSION.md`**. You may use different parameters (i.e a separate launch file) for the on-car deployment.

### Submitting

We'll be using Classroom 50 throughout the semester to manage submissions for lab assignments. You can commit and push your work as often as you need, but a plain push does **not** count as a submission. When you're ready to submit, push a tag named `submission`:

```bash
git push                            # your commits
git tag submission
git push origin submission          # this triggers the autograder
```

The autograder builds your package, probes your controller with synthetic scans, and drives it around both Levine maps in the simulator, then posts your score as a **Release** on your repo (check the Releases page or the commit's status check a few minutes after you tag). To resubmit, move the tag to a new commit:

```bash
git tag -f submission
git push --force origin submission
```
The last ``submission`` push before the deadline is counted as your final submission and its grade will be your lab's grade.

**The autograder finds your work by name.** Use the names the deliverables specify: package `gap_follow` with an executable it can start with `ros2 run gap_follow <executable>` (the skeleton's `reactive_node`), subscribing `/scan` and publishing `/drive`. Otherwise, the autograder will not be able to grade your work and your submission may get the wrong grade.

### VI. Grading Rubric

- Compilation: **10** Points (autograded)
- Implemented Find-Max Gap: **30** Points (autograded without the simulator: your node is fed scans of a pillar ahead of the car and of a corridor with the car close to one wall, each situation and its mirror image, and must steer toward the wider gap every time)
- Implemented Find best point: **30** Points (autograded without the simulator: a dead end with the corridor continuing to one side, mirrored; your node must aim into the exit)
- Levine blocked Simulation: **10** Points (autograded in simulation: one counter-clockwise lap of `levine_blocked` without touching a wall; a run that ends early earns partial credit for the fraction of the loop covered)
- Levine obstacles Simulation: **5** Points (autograded in simulation: `levine_obs` counter-clockwise from the east hallway, through at least 3 corners without touching anything; 1 or 2 corners earn partial credit)
- Levine obstacles bonus - all 4 corners: **5** Points (autograded in simulation: a full clean lap of `levine_obs`, counter-clockwise from the same start; the lap time goes to the obstacle-course leaderboard)
- Real-car Levine Video: **15** Points (TA-graded from the link in `SUBMISSION.md`: YouTube unlisted, or Google Drive shared as "Anyone with the link can view")

### VII. Extra Resources

UNC Follow the Gap Video: https://youtu.be/ctTJHueaTcY
