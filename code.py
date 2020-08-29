# CircuitPython Joystick Controller for Elite: Dangerous landings
# Copyright (c) 2020, CMDR Cal Dallicort [ALDN]
#
# This software released under the MIT License
#
# This module translates a potentiometer or other scaling analog input
#  to a joystick axis. It is specifically designed for use with
#  Elite: Dangerous but is also practical as, e.g., an elevator trim in
#  MS Flight Simulator.
#
# The variable "reduce_downward_input", when True (default), reduces
#  the effective input in the negative axis only by a factor of 5
#  to permit better fine-tuning of the descent rate.
#  Set to False on line 29 to revert to the full input range.
#  The positive axis is always at full strength.
#
# The variable "invert_input_direction", when True (not default),
#  swaps the positive and negative ends of the potentiometer. This is
#  useful to align the intended downward direction with the reduced
#  downward input. Set on line 32.
#
# This outputs only one joystick axis (the z axis). The other three
#  axes (x, y, rz) and all 16 buttons are not implemented.

import board
import analogio
import usb_hid
from adafruit_hid.gamepad import Gamepad

# set True to reduce the downward input by a factor of 5
reduce_downward_input = True

# set True to switch the positive and negative ends of the input range
invert_input_direction = False

# define the gamepad HID
gp = Gamepad(usb_hid.devices)

# define the analog input
analog_slide = analogio.AnalogIn(board.A0)

# map the raw unsigned 16-bit analog input to a signed 8-bit output
# includes parameters for the adjustments noted in the header
def range_map(raw_input, in_min=0, in_max=65535, out_min=-127, out_max=127, reduce_down=True, invert_input=False):
    adjusted_range = (raw_input - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    # invert before modulating downward input value
    if invert_input == True:
        adjusted_range = -1 * adjusted_range
    # modulate downward input value
    if (adjusted_range < 0) and (reduce_down == True):
        adjusted_range = adjusted_range // 5
    return adjusted_range

# Primary loop
while True:
    # determine signed 8-bit output value
    adjusted_output = range_map(raw_input=analog_slide.value, reduce_down=reduce_downward_input, invert_input=invert_input_direction)
    # send output value as joystick z axis
    gp.move_joysticks(z = adjusted_output )