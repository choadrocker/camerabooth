## Start with the latest raspbian (2017-04-10 is what I used)

Boot, run raspi-config and enable the camera and ssh, set w/e else you like (locale, tz, keyboard, etc)

<!--https://raspberrypi.stackexchange.com/questions/14229/how-can-i-enable-the-camera-without-using-raspi-config-->

```
sudo -i
apt-get update && sudo apt-get upgrade -y
apt-get install -y python-pygame
echo "bcm2835-v4l2" >> /etc/modules-load.d/modules.conf
reboot
```

## Install picam

https://github.com/iizukanao/picam

### Read about ft5406 lib
https://github.com/pimoroni/python-multitouch

ft5406 has been patched to run with python 2.7


Use `arecord -l` to make sure your usb sound card is detected



