#!/bin/bash

# esptool.py --port /dev/ttyUSB0 erase_flash

esptool.py  --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20190618-v1.11-47-g1a51fc9dd.bin
