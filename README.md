# termux-permissions-fixer

This scrip can make an executable file in bin directory. This file will fix permissions if you run apt, pip or etc.
***
**IT IS BETTER NOT TO RUN ANY PACKAGE MANAGER AS ROOT**
***
## Dependences
Python3
## Have your permissions already broken?
Run next commands in *Termux (failsafe)* to fix:
1. ```su -c chown -R $(whoami):$(whoami) /data/data/com.termux/```
2. ```su -c /system/bin/ls -alZ $(maketmp)```
3. Copy such fragment ```u:object_r:app_data_file:s0:cX,cY```
4. ```su -c chcon -R %your_fragment /data/data/com.termux/```