POLLING_RATE = 1000
ICE_MODE_HOTKEY = 'DPAD_DOWN'
PRECISION_MODE_HOTKEY = 'DPAD_RIGHT'
FILTER = BUTTON_DPAD_DOWN + BUTTON_DPAD_RIGHT

if __name__ == "__main__":
    from XInput import *
    from time import sleep
    import vgamepad as vg

    gamepad = vg.VX360Gamepad()

    gamepad.mode = 0
    gamepad.x = 0
    gamepad.y = 0

    def ToggleMode(mode):
        if gamepad.mode == mode:
            gamepad.mode = 0
        else:
            gamepad.mode = mode

    def UpdateStick(x, y):
        gamepad.x = x
        gamepad.y = y

        if gamepad.mode == 1:
            if abs(y) * 0.5 >= abs(x):
                x = 0
            if abs(x) * 0.5 >= abs(y):
                y = 0
            if x > 0:
                x = 1
            elif x < 0:
                x = -1
            if y > 0:
                y = 1
            elif y < 0:
                y = -1
        elif gamepad.mode == 2:
            if x > 0:
                x = (abs(x) ** 2) * 1
            elif x < 0:
                x = (abs(x) ** 2) * -1
            if y > 0:
                y = (abs(y) ** 2) * 1
            elif y < 0:
                y = (abs(y) ** 2) * -1

            # fix for diagonal bug
            total = abs(x) + abs(y)
            if total != 0:
                _x = x * (1 + abs(y)/total)
                _y = y * (1 + abs(x)/total)

                x = _x
                y = _y
        
        gamepad.left_joystick_float(x_value_float=x, y_value_float=y)

        gamepad.update()

    class MyHandler(EventHandler):
        def process_button_event(self, event):
            if event.type == 3:
                if event.button == ICE_MODE_HOTKEY:
                    ToggleMode(1)
                    UpdateStick(gamepad.x, gamepad.y)
                if event.button == PRECISION_MODE_HOTKEY:
                    ToggleMode(2)
                    UpdateStick(gamepad.x, gamepad.y)

            gamepad.update()

        def process_trigger_event(self, event):
            pass

        def process_stick_event(self, event):
            UpdateStick(event.x, event.y)

        def process_connection_event(self, event):
            pass

    filter = STICK_LEFT + FILTER
    my_handler = MyHandler(0)
    my_handler.set_filter(filter)
    my_gamepad_thread = GamepadThread(my_handler)

    while True:
        sleep(1/POLLING_RATE)