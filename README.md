## Video recording camera booth

### Hardware used
* A Raspberry Pi (the 3 B+ was used)
* A Micro SD card (64GB was used)
* The Raspberry Pi 7" touchscreen display
* The Raspberry Pi camera module (V2 was used)
* A 24" Raspberry Pi camera cable (optional)
* A USB sound card (C-Media Electronics, Inc. Audio Adapter (ID 0d8c:000c) was used)
* A mircophone with a 3.5mm jack (https://www.amazon.com/gp/product/B016C4ZG74 was used)
* A dual port 2.1A/5V USB charger
* 2 6ft USB to MicroUSB cables capable of charging


### Assembly
Follow the instructions to attach the display to your Raspberry Pi
Install Raspberrian to your MicroSD card (2018-06-27-raspbian-stretch-lite was used)

Boot, run `raspi-config` and enable the camera, ssh, and set w/e else you like (locale, tz, keyboard, etc)

<!--https://raspberrypi.stackexchange.com/questions/14229/how-can-i-enable-the-camera-without-using-raspi-config-->

Log in to the Raspberry Pi and install the nessecary software:
```
sudo apt-get update
sudo apt-get install -y python-pygame git
sudo echo "bcm2835-v4l2" >> /etc/modules-load.d/modules.conf
sudo reboot
```

### Install picam (picam-1.4.6-binary was used)
Follow directions at:
https://github.com/iizukanao/picam#using-a-binary-release

### Check out *this* repo
`git clone https://github.com/choadrocker/camerabooth.git`

### Copy the etc files into place to run picam as a service
<!--from https://github.com/iizukanao/picam/tree/master/etc-->
```
sudo cp camerabooth/contrib/etc_init.d_picam /etc/init.d/picam
sudo cp camerabooth/contrib/etc_default_picam /etc/default/picam
sudo update-rc.d picam defaults
sudo service picam start
```

Use `arecord -l` to make sure your usb sound card is detected and set properly in `/etc/default/picam`
Adjust mic gain if needed with `alsamixer`

### Add the following to /etc/rc.local above the `exit 0`
```
# disable the screen from shutting off
sudo sh -c "TERM=linux setterm -blank 0 >/dev/tty0"

# to start the app at boot
python /home/pi/camerabooth/camerabooth.py
```

### Enjoy!
Videos will end up in `/home/pi/picam/record/archive`
A 30 second video is about 10 MB

### Notes
The display is fairly power hungry, be sure to plug both the Raspberry Pi and the display in to USB power

Any USB sound card should work as long as it's recognized






