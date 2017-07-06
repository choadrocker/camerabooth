## Start with the latest raspbian (2017-04-10 is what I used)

Boot, run raspi-config and enable the camera, ssh, and set w/e else you like (locale, tz, keyboard, etc)

<!--https://raspberrypi.stackexchange.com/questions/14229/how-can-i-enable-the-camera-without-using-raspi-config-->

```
sudo -i
apt-get update
apt-get install -y python-pygame git
echo "bcm2835-v4l2" >> /etc/modules-load.d/modules.conf
reboot
```

## Install picam (picam-1.4.6-binary.tar.xz is what I used)
https://github.com/iizukanao/picam#using-a-binary-release

## Check out this repo
`git clone https://github.com/choadrocker/camerabooth.git'

## Copy the etc files into place to run picam as a service
<!--from https://github.com/iizukanao/picam/tree/master/etc-->
```
sudo cp camerabooth/ansible/camerabooth/files/etc/init.d/picam /etc/init.d/
sudo cp camerabooth/ansible/camerabooth/files/etc/default/picam /etc/default/
sudo update-rc.d picam defaults
sudo service picam start
```

Use `arecord -l` to make sure your usb sound card is detected and set properly in /etc/default/picam

## Add the following to /etc/rc.local above the `exit 0`
```
# the disable the screen shutting off
sudo sh -c "TERM=linux setterm -blank 0 >/dev/tty0"

# to start the app at boot
python /home/pi/camerabooth/camerabooth.py
```
