# tcs34725-sensor
Python code to use the Adafruit TCS34725 color sensor with a Raspberry Pi 

## Installation of additional software libraries to use the TCS34725 on a Raspberry Pi

### Install smbus package for I2C library
    $ sudo apt-get install python-smbus

### Install Adafruit TCS34725 driver library
    $ sudo pip install adafruit-tcs34725

    # Alternatively, you may could clone the Adafruit source tree from here if you
    # think that you may need to update the driver code:
    git clone https://github.com/adafruit/Adafruit_Python_TCS34725.git

### Enable the I2C interface on the Raspberry Pi
    IMPORTANT: You must also enable the I2C interface on the Raspberry Pi, as it 
               is disabled by default. This is done via the 'raspi-config' utility.
               Launch the utility, select 'Interfacing Options', then I2C, and then 
               enable the interface
    $ sudo raspi-config

### Run the sensortest.py utility as follows.
    python sensortest.py --help
    
    usage: sensortest.py [-h] [-i INTEGRATION_TIME] [-g GAIN] [-l LED_CTRL_PIN]
                         [-d] [-t TIME_INTERVAL]
                         
    optional arguments:
      -h, --help            show this help message and exit
      -i INTEGRATION_TIME, --integration_time INTEGRATION_TIME
                            Valid options: 2.4, 24, 50, 101, 154, 700 (default=50)
      -g GAIN, --gain GAIN  Valid options: 1, 4, 16, 60 (default=4)
      -l LED_CTRL_PIN, --led_ctrl_pin LED_CTRL_PIN
                            GPIO pin wired to the TCS LED control (default=26)
      -d, --led_disable     Turn off LED on TCS
      -t TIME_INTERVAL, --time_interval TIME_INTERVAL
                            Time interval between color measurements (default=0.1)
