#!/bin/bash

echo "This script will install a library that will intercept pen events and smooth them."
echo
echo "If you haven't set up public key authentication on your remarkable yet, now would"
echo "be a good time to do so (otherwise you'll have to type your password multiple"
echo "times)."
echo
echo "Either way, make sure you have your remarkable password written down somewhere, you"
echo "might otherwise risk to lock yourself out if the GUI does not start up anymore."

echo
read -p "Enter the hostname or IP address of your remarkable device [remarkable]:" remarkable
remarkable=${remarkable:-remarkable}

if [[ "$(ssh root@$remarkable cat /sys/devices/soc0/machine)" == "reMarkable 2*" ]];
then \
  device=rm2
else \
  device=rm1
fi

echo
echo "Chose the amount of smoothing you want to apply to pen events. Larger values will"
echo "smooth more, but will also lead to larger perceived latencies."
echo
echo "Entering 0 will uninstall the library."
echo
read -p "Amount of smoothing (value between 2 and 32, or 0) [8]:" ring_size
ring_size=${ring_size:-8}

if [ "${ring_size}" -eq "0" ]
then \
  echo "Uninstalling ReCept..."
  ssh root@$remarkable "grep -qxF 'Environment=LD_PRELOAD=/usr/lib/librecept.so' /lib/systemd/system/xochitl.service && sed -i '/Environment=LD_PRELOAD=\/usr\/lib\/librecept.so/d' /lib/systemd/system/xochitl.service"
else \
  echo "Installing ReCept with ring size ${ring_size}..."
  scp ./build/$device/librecept_rs${ring_size}.so root@$remarkable:/usr/lib/librecept.so
  ssh root@$remarkable "grep -qxF 'Environment=LD_PRELOAD=/usr/lib/librecept.so' /lib/systemd/system/xochitl.service || sed -i 's#\[Service\]#[Service]\nEnvironment=LD_PRELOAD=/usr/lib/librecept.so#' /lib/systemd/system/xochitl.service"
fi

echo "...done."
echo "Restarting xochitl..."
ssh root@$remarkable "systemctl daemon-reload; systemctl restart xochitl"
echo "...done."
