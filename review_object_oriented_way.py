import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from functools import partial
import threading
import time
import imutils

class Umpire(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 450
        self.title = "Video and Image Processing"
        self.stream = cv2.VideoCapture("clip1.mp4")

    def play(self, speed):
        # Play the video in reverse mode
        frame1 = self.stream.get(cv2.CAP_PROP_POS_FRAMES)
        self.stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

        grabbed, frame = self.stream.read()
        if not grabbed:
            exit()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=self.width, height=self.height)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        canvas.create_text(650, 26, fill="white", font="Times 26 bold", text="Decision Pending")

    def pending(self, decision):

        # Display decision pending image
        frame = cv2.cvtColor(cv2.imread("pending.png"), cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=self.width, height=self.height)
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
        frame = imutils.resize(frame, width=self.width, height=self.height)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)

    def out(self):
        thread = threading.Thread(target=self.pending, args=("out",))
        thread.daemon = 1
        thread.start()

    def not_out(self):
        thread = threading.Thread(target=self.pending, args=("not out",))
        thread.daemon = 1
        thread.start()

    def buttons(self, text, command):
        tkinter.Button(text=text, width=50, command=command).pack()


# Tkinter gui starts here
window = Umpire()
cv_img = cv2.cvtColor(cv2.imread("back.png"), cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width=window.width, height=window.height)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0, 0, anchor=tkinter.NW, image=photo)
canvas.pack()
window.buttons("<< Rewind(fast mode):", partial(window.play, -15))
window.buttons("<< Rewind(slow mode):", partial(window.play, -2))
window.buttons("<< Forward(slow mode):", partial(window.play, 0.5))
window.buttons("<< Forward(fast mode):", partial(window.play, 15))
window.buttons("Give: Out", partial(window.out))
window.buttons("Give: Not Out", partial(window.not_out))
window.mainloop()