Events
======

Events come separately for x, y, pressure, distance, tilt_x, tilt_y

However, x and y are mostly paired (x first, then y), with the same timestamp
Except if either x or y do not change, then the event is omitted (guessing from
drawing straight lines)

Sync event (type == code == 0) marks end of frame -> can be used to infer
missing x/y event

Event CSV should contain for each frame x, y, pressure, distance, tilt_x,
tilt_y

Ideas
=====

Adaptive Kalman Filter
----------------------

Change measurement noise as a function of speed. Naive version (scaling with
inverse of speed) is not good.

Adaptive Smoothing
------------------

Use the Kalman filter *only* for the speed estimate. Decide on ring buffer size
based on speed.

Slow horizontal line: speed around 2-3

Median Filter
-------------

Seems to be pretty good (we use it for the "gold standard"). Could be combined
with adaptive smoothing.

Results
=======

Hello World
-----------

### Baseline (mean filter with size 15):

  mean distance : 2.488560919562702
  max distance  : 10.198039027185569
  mean latency  : 13393.816666666668

### Kalman

  Best Kalman is (0.005, 1.0) with:
  mean distance : 2.0189294393408064
  max distance  : 19.32973032570337
  mean latency  : 135.8908496732026

Horizontal Line
---------------

### Baseline (mean filter with size 15):

  mean distance : 0.9786546371486243
  mean latency  : 15333.48494353827

### Kalman

  Best Kalman is (0.001, 19.0) with:
  mean distance : 2.2236545733927895
  mean latency  : -936.7735257214555
