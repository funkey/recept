ReCept: Remarkable Intercept
============================

A small library to intercept and smooth pen events on the [reMarkable
2](https://remarkable.com/) tablet. This fixes the infamous "jagged lines"
issue some users of the reMarkable 2 experience.

![before vs after](images/before_after.png)

Disclaimer
----------

This is not an official reMarkable product, and I am in no way affiliated with
reMarkable. I release this library in the hope that it is helpful to others. I
can make no guarantee that it works as intended. There might be bugs leading to
device crashes.

Installation
------------

You need access to a Linux machine to install the fix. On that machine:

1. Connect your reMarkable 2 with the USB-C cable.
2. Clone this repository, i.e., run `git clone https://github.com/funkey/recept` in a terminal.
3. Change into the repository with `cd recept`.
4. Run `./install.sh`.

The install script will make several `ssh` connections to your device. For
that, it needs to know the IP address or hostname of your device. If you
haven't set up public key authentication before, it will also ask for a
password. You can find both the IP address and password in "Settings" -> "Help"
-> "Copyrights and licenses", at the bottom.

If you want to uninstall the fix, simply enter `0` when asked for the smoothing
value in the install script.

Will it increase the latency?
-----------------------------

In short, yes. The pen events themselves are not delayed (the filter itself
consists only of a handful of integer operations, which are likely negligible).
However, since we forward the average position of the past `N` events instead
of the actual event, the reported position is somewhere close to the `N/2`-last
event received. How much that actually increases latency depends on how fast
events come in. As an example, if the pen sends 1000 events per second and the
filter size `N` is 8, the mean will trail the actual pen position by around 4
milliseconds. This calculation assumes isochronous events, which might not be
the case.

How does it work?
-----------------

`ReCept` uses the `LD_PRELOAD` trick, which in this case intercepts calls to
`open` and `read`. Whenever `/dev/input/event1` is opened by `xochitl` (the GUI
running on the tablet), `librecept` remembers the file handle. Subsequent
`read`s from this handle are transparently filtered with a moving average of
size 16 by default.

Building
--------

To build for both devices run the following:

```bash
source /opt/codex/rm10x/3.1.15/environment-setup-cortexa9hf-neon-remarkable-linux-gnueabi
make
```

To only build for rM1 run the following:

```bash
source /opt/codex/rm10x/3.1.15/environment-setup-cortexa9hf-neon-remarkable-linux-gnueabi
make rm1
```

To only build for rM1 run the following:

```bash
source /opt/codex/rm10x/3.1.15/environment-setup-cortexa9hf-neon-remarkable-linux-gnueabi
make rm2
```
