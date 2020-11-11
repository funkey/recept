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

scp ./librecept.so root@$remarkable:/usr/lib/
ssh $remarkable "grep -qxF 'Environment=LD_PRELOAD=/usr/lib/librecept.so' /lib/systemd/system/xochitl.service || sed -i 's#\[Service\]#[Service]\nEnvironment=LD_PRELOAD=/usr/lib/librecept.so#' /lib/systemd/system/xochitl.service"
ssh $remarkable "systemctl daemon-reload; systemctl restart xochitl"
