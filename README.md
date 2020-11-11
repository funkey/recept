ReCept: Remarkable Intercept
============================

A small library to intercept and smooth pen events on the [reMarkable
2](https://remarkable.com/) tablet. This fixes the infamous "jagged lines"
issue some users of the reMarkable 2 experience.

![before vs after](images/before_after.png)

Installation
------------

Clone this repository and run `./install.sh`.

How does it work?
-----------------

`ReCept` uses the `LD_PRELOAD` trick, which in this case intercepts calls to
`open` and `read`. Whenever `/dev/input/event1` is opened by `xochitl` (the GUI
running on the tablet), `librecept` remembers the file handle. Subsequent
`read`s from this handle are transparently filtered with a moving average of
size 16 by default.
