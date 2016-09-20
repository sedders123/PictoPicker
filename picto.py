import evdev
from getch import getch
import os


def get_input_devices():
    devices = []
    for d in range(20):
        filename = "/dev/input/event%d" % (d,)
        if os.path.exists(filename):
            dev = evdev.InputDevice(filename)
            devices.append(dev)
    return devices


def filter_duplicate_keyboards(keyboards):
    actual_keyboards = []
    for keyboard in keyboards:
        if keyboard.phys[-1:] == "0":
            actual_keyboards.append(keyboard)
    return actual_keyboards



def get_external_keyboards():
    complete = False
    keyboards = []
    for i in range(13):
        devices = get_input_devices()
        if not complete:
            print("Please connect keyboard {}".format(i))
            keyboard_found = False
            while not keyboard_found:
                current_devices = get_input_devices()
                for device in current_devices:
                    if device not in devices:
                        keyboards.append(device)
                        print(device)
                        keyboard_found = True
            print("Press enter to add another keboard")
            print("Press ` to end adding keboards")
            char = getch()
            if char == "`":
                complete = True
        if i == 13:
            complete = True
    actual_keyboards = filter_duplicate_keyboards(keyboards)
    return actual_keyboards


def main():
    keyboards = get_external_keyboards()
    monitor_keyboards(keyboards)

if __name__ == '__main__':
    main()
