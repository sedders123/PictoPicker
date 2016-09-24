import evdev
from getch import getch
import os
import asyncio


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
    enumerated_keyboards = get_enumerated_keyboards(actual_keyboards)
    return enumerated_keyboards


def get_enumerated_keyboards(keyboards):
    enumerated_keyboards = []
    for kbd_no, keyboard in enumerate(keyboards):
        list_object = (kbd_no, keyboard)
        enumerated_keyboards.append(list_object)
    return enumerated_keyboards


async def print_events(kbd_no, keyboard):
    async for event in keyboard.async_read_loop():
        try:
            print(kbd_no, evdev.events.KeyEvent(event), sep=': ')
        except:
            print("error")


def monitor_keyboards(keyboards):
    for kbd_no, keyboard in keyboards:
        asyncio.ensure_future(print_events(kbd_no, keyboard))
    loop = asyncio.get_event_loop()
    loop.run_forever()


def main():
    keyboards = get_external_keyboards()
    monitor_keyboards(keyboards)


if __name__ == '__main__':
    main()
