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

Test in the [f1tenth_gym_ros](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-jazzy) simulator on two of its maps: `levine_blocked`, the empty Levine loop with its doorways sealed, and `levine_obs`, the loop with its corner doorways bricked up and thirteen obstacles added (a slalom of boxes and an ellipse on the south hallway, two triangles and a box on the north hallway) that are relatively hard to navigate through. Pick one with `map_path: 'maps/levine_blocked'` or `map_path: 'maps/levine_obs'` in `config/sim.yaml`. Both come with a centerline, so the simulator counts your laps (`/ego_racecar/lap_count`, and a "completed lap" line in the bridge log). The autograder drives your node on the same two maps: `levine_blocked` counter-clockwise from the simulator's stock start pose (`sx: -12.0, sy: 0.0, stheta: 0.0`), on the south hallway heading east, 12 m before the finish line, so all three laps are flying laps and the lap times it reports are the ones your bridge log prints (`completed lap N, last lap X s`); `levine_obs` counter-clockwise too, from the east hallway just past its south corner (`sx: 9.96, sy: 2.8, stheta: 1.5708` in `config/sim.yaml`), heading north, so the north-hallway obstacles and three corners come first and only a full lap has to thread the south-hallway slalom. Test both directions: an obstacle that is easy from one side can be a trap from the other (the L-shaped wall on the north hallway is a dead-end pocket with the way through above it).

Your node must subscribe to `/scan` and publish `AckermannDriveStamped` on `/drive`.

**One launch file per map.** The autograder starts your code with the two launch files in `gap_follow/launch/`, and nothing else:

```bash
ros2 launch gap_follow levine_blocked_launch.py   # the three timed laps
ros2 launch gap_follow levine_obs_launch.py       # the obstacle course (and the scan checks)
```

Each one is yours to edit: set `EXECUTABLE` to the node you wrote (`reactive_node.py` for Python, `reactive_node` for C++), give each map its own parameter values (a fast tuning for the empty loop, a careful one for the obstacles: one submission now covers both), and start as many nodes as you like, in either language (a gap finder in Python and a controller in C++, say). Start your own nodes only: the autograder runs the simulator. `CMakeLists.txt` must install the folder, `install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})`; the skeleton does. If your team accepted the lab before the launch files were added, copy the two files from [the template](https://github.com/f1tenth/f1tenth_lab4_template/tree/main/gap_follow/launch) and add that line.

Without launch files the autograder falls back to a plain `ros2 run gap_follow <executable>` with no parameter file, so the tuned values must then be your node's defaults. Line F of your result tells you which way each run was started.

Tip: a gap is only worth aiming at if the car fits through it; the closest-point bubble alone does not tell you that.

### V. Deliverables and Submission

**This lab is done in teams**, and from here on every lab is. Your team is already formed — you do not create one or invite anyone.

First upgrade the CLI:

```bash
gh extension upgrade gh-student
gh student --version                # v1.41.0 or newer
```

Then **every member of the team runs the same command**:

```bash
gh student accept RoboRacer-Class ese-6150 lab-4-follow-the-gap
```

Whoever runs it first creates the team's shared repository, `ese-6150-lab-4-follow-the-gap-group-<n>`; everyone else gets `Repository already exists` and the same URL. There are no invites to send — your push access comes from your team. To see who is on your team:

```bash
gh student team list RoboRacer-Class ese-6150 lab-4-follow-the-gap
```

If accept tells you your teacher assigns the groups and you are not in one, ask a TA rather than creating anything yourself.

All of you push to that one repository, so **pull before you push**. One submission is the whole team's submission, and every member gets the same grade.

**Deliverable 1**: After you're finished, update the entire skeleton package directory with your `gap_follow` package and directly commit and push to your team's repository. Your committed code should start and run in simulation smoothly, this includes building as a package with any dependencies included as part of the ``package.xml``. The basic requirement is that your car should be able to drive three laps in a row of the `levine_blocked` map without touching a wall (the autograder times each lap and the leaderboard keeps your team's fastest), and through at least 3 corners of the `levine_obs` map. You get 5 bonus points if your implementation is able to complete all 4 corners and keeps lapping through the map. The autograder watches both runs in the simulator, so no screencast is needed for them.

**Deliverable 2**: Take a video of your team's algorithm running on the real car — one video for the team. Upload it to YouTube (unlisted) or Google Drive — for Drive, set sharing to **"Anyone with the link can view"** or we cannot grade it — and include the link in **`SUBMISSION.md`**. You may use different parameters (i.e a separate launch file) for the on-car deployment.

### Submitting

We'll be using Classroom 50 throughout the semester to manage submissions for lab assignments. You can commit and push your work as often as you need, but a plain push does **not** count as a submission. When your team is ready to submit, any one of you pushes a tag named `submission` — it counts for the whole team, so agree on the commit first:

```bash
# Make sure you've pulled before or switch branches
git push                            # your commits
git tag submission
git push origin submission          # this triggers the autograder
```

The autograder builds your package, probes your controller with synthetic scans, and drives it around both Levine maps in the simulator, then posts your score as a **Release** on your repo (check the Releases page or the commit's status check a few minutes after you tag). To resubmit, move the tag to a new commit:

```bash
git tag -f submission
git push --force origin submission
```
The best scored ``submission`` push is counted as your team's final submission, and its grade is every member's grade for the lab. A careful tuning for the obstacle map and a fast one for the `levine_blocked` leaderboard fit in one submission: that is what the two launch files are for.

**The autograder finds your work by name.** Use the names the deliverables specify: package `gap_follow`, launch files `levine_blocked_launch.py` and `levine_obs_launch.py` (or, without them, an executable it can start with `ros2 run gap_follow <executable>`, the skeleton's `reactive_node`), subscribing `/scan` and publishing `/drive`. Otherwise, the autograder will not be able to grade your work and your submission may get the wrong grade.

### VI. Grading Rubric

- Compilation: **10** Points (autograded)
- Implemented Find-Max Gap: **30** Points (autograded without the simulator: your node is fed scans of a pillar ahead of the car and of a corridor with the car close to one wall, each situation and its mirror image, and must steer toward the wider gap every time)
- Implemented Find best point: **30** Points (autograded without the simulator: a dead end with the corridor continuing to one side, mirrored; your node must aim into the exit)
- Levine blocked Simulation: **10** Points (autograded in simulation: three counter-clockwise laps of `levine_blocked` in a row without touching a wall; a run that ends early earns partial credit for the fraction of the three-lap distance covered; the fastest of the three laps goes to the leaderboard, where your team races under its own number)
- Levine obstacles Simulation: **5** Points (autograded in simulation: `levine_obs` counter-clockwise from the east hallway, through at least 3 corners without touching anything; 1 or 2 corners earn partial credit)
- Levine obstacles bonus - all 4 corners: **5** Points (autograded in simulation: a full clean lap of `levine_obs`, counter-clockwise from the same start; the lap time goes to the obstacle-course leaderboard)
- Real-car Levine Video: **15** Points (TA-graded from the link in `SUBMISSION.md`: YouTube unlisted, or Google Drive shared as "Anyone with the link can view")

### VII. Extra Resources

UNC Follow the Gap Video: https://youtu.be/ctTJHueaTcY
