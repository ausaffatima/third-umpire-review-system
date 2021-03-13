import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import time
import imutils

stream = cv2.VideoCapture("clip1.mp4")

def play(speed):

    # Play the video in reverse mode
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        exit()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    canvas.create_text(650, 26, fill="white", font="Times 26 bold", text="Decision Pending")

def pending(decision):

    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    # 2. Wait for 1 second
    time.sleep(1.5)

    # Display out/notout image
    if decision == 'out':
        decisionImg = "out.png"
    else:
        decisionImg = "notout.png"
    frame = cv2.cvtColor(cv2.imread(decisionImg), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width=WIDTH, height=HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()

# Width and height of our main screen
WIDTH = 800
HEIGHT = 450

# Tkinter gui starts here
window = tkinter.Tk()
window.title("Video and Image Processing")
cv_img = cv2.cvtColor(cv2.imread("back.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, ancho=tkinter.NW, image=photo)
canvas.pack()

# Buttons to control playback
btn = tkinter.Button(window, text="<< Rewind(fast mode):", width=50, command=partial(play, -15))
btn.pack()

btn = tkinter.Button(window, text="<< Rewind(slow mode):", width=50, command=partial(play, -2))
btn.pack()

btn = tkinter.Button(window, text="Forward(slow mode): >>", width=50, command=partial(play, 0.5))
btn.pack()

btn = tkinter.Button(window, text="Forward(fast mode): >>", width=50, command=partial(play, 15))
btn.pack()

btn = tkinter.Button(window, text="Give: Out", width=50, command=out)
btn.pack()

btn = tkinter.Button(window, text="Give: Not Out", width=50, command=not_out)
btn.pack()
window.mainloop()
