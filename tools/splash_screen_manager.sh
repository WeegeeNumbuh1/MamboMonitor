#!/bin/bash
systemctl stop mambo-bootsplash.service >/dev/null 2>&1
kill -15 $(ps aux | grep 'splash-sysinit.py' | awk '{print $2}') >/dev/null 2>&1
exit 0