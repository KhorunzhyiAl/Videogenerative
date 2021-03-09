import cv2
import numpy as np
import time


rea = cv2.VideoCapture("input/input_vid.mp4")

if not rea.isOpened():
    print("error opening video")

ix = int(rea.get(cv2.CAP_PROP_FRAME_WIDTH))
iy = int(rea.get(cv2.CAP_PROP_FRAME_HEIGHT))
it = int(rea.get(cv2.CAP_PROP_FRAME_COUNT))
ox = it
oy = iy
ot = ix

wri = cv2.VideoWriter("output/out.avi", cv2.VideoWriter_fourcc(*"MJPG"), 30.0, (ox, oy))

curr_x = 0

# we can't fit the entire video into the memory, but we want to get as much of it as possible per iteration
step = 300

while curr_x + step <= ix:
    print(f'x: {curr_x}/{ix}')

    arr = np.empty((oy, ox, step, 3), dtype="uint8")
    curr_t = 0
    while rea.isOpened():
        if curr_t % 200 == 0:
            print(f"\tt: {curr_t}")

        ret, frame = rea.read()
        if ret != True:
            break
        part = frame[:, curr_x:curr_x + step]
        arr[:, curr_t, :, :] = part
        curr_t += 1

    print("writing frames...")
    for i in range(step):
        if i % (step / 5) == 0:
            print(f"\ti: {i}/{step}")
        new_frame = arr[:, :, i, :]
        wri.write(new_frame)
 
    rea.set(cv2.CAP_PROP_POS_FRAMES, 0)
    curr_x += step
    print("done")

