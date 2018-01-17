# Simple demo of reading color data with the TCS34725 sensor.
# Will read the color from the sensor and print it out along with lux and
# color temperature.
#
# Derived from Adafruit simpletest.py, originally written by Tony DiCola.
# License: Public Domain

import argparse
import time

# import the Raspberry Pi GPIO library
import RPi.GPIO as GPIO

# Import the TCS34725 module.
import Adafruit_TCS34725

# import the library to allow us to access the I2C bus
import smbus

# access function to obtain a valid integration time constant from an option string
def get_tcs_int_time( opt_str ):
    tcs_int_time_opts = {
        '2.4' : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_2_4MS,
        '24'  : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_24MS,
        '50'  : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_50MS,
        '101' : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_101MS,
        '154' : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_154MS,
        '700' : Adafruit_TCS34725.TCS34725_INTEGRATIONTIME_700MS
    }

    try:
        int_time = tcs_int_time_opts[opt_str]
    except:
        print 'Invalid integration time option: %s, defaulting to 2.4ms' % opt_str
        int_time = tcs_int_time_opts['2.4']
    return int_time

# access function to obtain a valid gain constant from an option string
def get_tcs_gain( opt_str ):
    tcs_gain_opts = {
        '1'  : Adafruit_TCS34725.TCS34725_GAIN_1X,
        '4'  : Adafruit_TCS34725.TCS34725_GAIN_4X,
        '16' : Adafruit_TCS34725.TCS34725_GAIN_16X,
        '60' : Adafruit_TCS34725.TCS34725_GAIN_60X
    }

    try:
        gain = tcs_gain_opts[opt_str]
    except:
        print 'Invalid gain option: %s, defaulting to 4X' % opt_str
        int_time = tcs_gain_opts['4']
    return gain

#
# class to encapsulate the TCS initialization and certain access functions
class TCS(object):

    def __init__( self,
                  int_time_opt='50', gain_opt='4', led_ctrl_pin=26, led_on=True ):

        # get the library constants for the gain and integration time from the option strings
        self._int_time = get_tcs_int_time( int_time_opt )
        self._gain = get_tcs_gain( gain_opt )

        print 'Initializing TCS with integration time: %sms, gain: %sX' % (int_time_opt, gain_opt)
        print 'TCS LED control pin: %s, Initial State: %s' % (led_ctrl_pin,led_on)

        # You can also override the I2C device address and/or bus with parameters:
        #self._tcs = Adafruit_TCS34725.TCS34725(integration_time, gain, address=0x30, busnum=2)

        self._tcs = Adafruit_TCS34725.TCS34725( integration_time=self._int_time, gain=self._gain )

        # Disable interrupts (can enable them by passing true, see the set_interrupt_limits function too).
        self._tcs.set_interrupt(False)

        # set up the GPIO pin to control the LED on the TCS module and turn the LED on if specified
        GPIO.setmode(GPIO.BCM)
        self._led_ctrl_pin = led_ctrl_pin
        if led_on:
            initial_state= GPIO.HIGH
        else:
            initial_state= GPIO.LOW
        GPIO.setup(self._led_ctrl_pin, GPIO.OUT, initial=initial_state)

    # set of functions to control the LED on the TCS color sensor
    def disable_led(self):
        GPIO.output(self._led_ctrl_pin, GPIO.LOW)

    def enable_led(self ):
        GPIO.output(self._led_ctrl_pin, GPIO.HIGH)

    def read_sensor(self):

        # Read the R, G, B, C color data.
        r, g, b, c = self._tcs.get_raw_data()

        # Calculate color temperature using utility functions.  You might also want to
        # check out the colormath library for much more complete/accurate color functions.
        color_temp = Adafruit_TCS34725.calculate_color_temperature(r, g, b)

        # Calculate lux with another utility function.
        lux = Adafruit_TCS34725.calculate_lux(r, g, b)

        # Print out the values.
        print('Color: red={0} green={1} blue={2} clear={3}, Temperature: {4} K, Luminosity: {0} lux'.format(r, g, b, c, color_temp, lux))

    def disable(self):
        # Put the chip back to low power sleep/disabled.
        self._tcs.disable()

    def set_interrupt(self, enable_flag):
        self._tcs.set_interrupt(enable_flag)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--integration_time', action='store', dest='integration_time', default='50',
                        help='Valid options: 2.4, 24, 50, 101, 154, 700 (default=50)')
    parser.add_argument('-g', '--gain', action='store', dest='gain', default='4',
                        help='Valid options: 1, 4, 16, 60 (default=4)')
    parser.add_argument('-l', '--led_ctrl_pin', action='store', dest='led_ctrl_pin', default=26,
                        help='GPIO pin wired to the TCS LED control (default=26)')
    parser.add_argument('-d', '--led_disable', action='store_false', dest='led_disable', default=True,
                        help='Turn off LED on TCS')
    parser.add_argument('-t', '--time_interval', action='store', dest='time_interval', type=float, default=0.1,
                        help='Time interval between color measurements (default=0.1)')

    options = parser.parse_args()

    done = False

    tcs = TCS(options.integration_time, options.gain, options.led_ctrl_pin,options.led_disable)

    while not done:
        try:
            tcs.read_sensor()
            time.sleep(options.time_interval)
        except KeyboardInterrupt:
            done = True

    print 'Disabling Sensor...'
    tcs.set_interrupt(True)
    tcs.disable()
    tcs.disable_led()

    print 'Done!'
