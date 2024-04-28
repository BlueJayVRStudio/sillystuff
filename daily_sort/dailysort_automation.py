from pynput.mouse import Listener as Lis
from pynput.mouse import Controller, Button
from pynput.keyboard import Listener, Key
import json
import time
import threading

### Use below to get the screen coordinates of the test tubes from top-left to bottom-right

# positions = []

# def on_move(x, y):
#     # print(f"Mouse moved to ({x}, {y})")
#     pass

# def on_click(x, y, button, pressed):
#     if pressed:
#         print(f"Mouse clicked at ({x}, {y}) with {button}")
#         if len(positions) < 12:
#             positions.append([x, y])
#         else:
#             print (positions)
#     else:
#         print(f"Mouse released at ({x}, {y}) with {button}")

# def on_scroll(x, y, dx, dy):
#     print(f"Mouse scrolled at ({x}, {y}) with {dx}, {dy} scroll")

# # Set up the listener:
# with Lis(
#         on_move=on_move,
#         on_click=on_click,
#         on_scroll=on_scroll) as listener:
#     listener.join()


### Use below for automation

positions = "[[1629, 381], [1691, 378], [1752, 375], [1813, 375], [1869, 376], [1931, 373], [1635, 558], [1691, 558], [1755, 560], [1805, 562], [1870, 567], [1923, 567]]"
moves = "[[0, 10], [2, 11], [4, 0], [4, 10], [5, 11], [3, 2], [6, 11], [6, 10], [6, 3], [7, 6], [8, 6], [5, 8], [0, 5], [0, 5], [0, 4], [2, 0], [2, 0], [9, 2], [9, 0], [3, 9], [3, 9], [1, 3], [1, 2], [1, 4], [9, 1], [9, 1], [9, 1], [8, 9], [8, 9], [8, 11], [2, 8], [2, 8], [2, 8], [4, 2], [4, 2], [4, 2], [4, 9], [3, 4], [3, 4], [3, 6], [5, 3], [5, 3], [5, 3], [4, 5], [4, 5], [7, 4], [7, 3], [4, 10], [7, 5]]"
positions = json.loads(positions)
moves = json.loads(moves)

mouse = Controller()
Exit = False

def on_press(key):
    global Exit
    if key == Key.esc:
        Exit = True
        print("exiting...")
        quit()

def on_release(key):
    pass

def start_listener():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

thread = threading.Thread(target=start_listener)
thread.start()

# reset button position
mouse.position = (1485, 603)
mouse.click(Button.left, 1)

for i in moves:
    if Exit:
        break
    tubepos1 = positions[i[0]]
    tubepos2 = positions[i[1]]

    # Start
    mouse.position = (tubepos1[0], tubepos1[1])
    mouse.click(Button.left, 1)
    # time.sleep(0.1)

    # End
    mouse.position = (tubepos2[0], tubepos2[1])
    mouse.click(Button.left, 1)
    # time.sleep(0.1)

