from tkinter import *
from pathlib import Path
import threading
import time

global room_rotation
room_rotation=0

# room types:
# 	S = sleeping (blue)
# 	A = activity (brick)
# 	U = utility (orange)
# 	O = outdoor (green)
# 	D = downstairs (dark)
# 	C = corridor (white)
# 	L = living (purple)
# 	F = food (yellow)


class Room:
	def __init__(self, filename, canvas, position):
		self.canvas = canvas
		self.filename = filename
		self.rotation = 0
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/filename)
		self.photoimg = self.photoimg.subsample(3)
		
		# canvas.tag_bind(self.photoimg, '<ButtonPress-1>', move_image)
		self.room_img = canvas.create_image(width_*position/8, height_*6/7, anchor=CENTER, image=self.photoimg)
		
		self.bind()

	def bind(self):
		self.canvas.tag_bind(self.room_img, '<Double-1>', lambda x, e = self.room_img: self.rotate_img(x))
		self.canvas.tag_bind(self.room_img, '<B1-Motion>', lambda x, e = self.room_img: self.move_img(x))

	def parse_room(self, filename):
		room_dict = {
			"type": filename[0],
			"size": int(filename[2:5]),
			"points": int(filename[6]),
			"connections": {
				"type": filename.split('c')[1][2],
				"points": int(filename.split('c')[1][0])
			},
			"rotation": int(filename.split('r')[1][:3])
		}
		return room_dict

	def move_img(self, e):
		# Needed to reset image position
		self.photoimg = self.photoimg.subsample(1)

		self.room_img = self.canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)
		self.bind()
		self.canvas.pack()
		global points_
		points_ = 4

	def rotate_img(self, e):
		self.rotation = (self.rotation + 90) % 360
		self.filename = self.filename.split('.')[0][:-3] + str(self.rotation).zfill(3) + ".png"
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/self.filename)
		self.photoimg = self.photoimg.subsample(3)
		self.room_img = self.canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)
		self.bind()
		self.canvas.pack()


def refresh(canvas):
	while True:
		canvas.update()
		time.sleep(0.01)	


def update_score(e, canvas, button_widget):
	global text_
	global score_
	canvas.delete(text_)
	text_ = canvas.create_text(200, 60, fill="darkblue", font="Times 30 italic bold", text="Your score is:" + str(score_ + points_))
	button_widget.bind("<Button-1>", lambda e: update_score(e, canvas, button_widget))

def main():
	global width_
	global height_
	global points_
	global score_
	width_ = 1400
	height_ = 800
	score_ = 0
	points_ = 0

	tk = Tk()
	background = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"wood.png")
	background = background.zoom(2, 2)
	
	# background = background.subsample(background.width(), background.height())
	canvas = Canvas(tk, width=width_, height=height_)
	bg_img = canvas.create_image(0, 0, image=background, anchor="nw")
	

	foyer = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/"yellow_foyer.png")
	foyer = foyer.subsample(3)
	canvas.create_image(width_/2, height_/2.5, anchor=CENTER, image=foyer)

	# global Sleeping_Room_Test
	# global Outdoor_Room_Test
	Sleeping_Room_Test = Room("queens_bedroom_r000.png", canvas, 1)
	Outdoor_Room_Test = Room("hundings_hut_r000.png", canvas, 2)
	Utility_Room_Test = Room("broom_closet_r000.png", canvas, 3)
	Downstairs_Room_Test = Room("bottomless_pit_r000.png", canvas, 4)
	Living_Room_Test = Room("drawing_room_r000.png", canvas, 5)
	Theater_Room = Room("theater_r000.png", canvas, 6)
	Nap_Room = Room("nap_room_r000.png", canvas, 7)


	global text_
	text_ = canvas.create_text(200, 60, fill="darkblue", font="Times 30 italic bold", text="Your score is: 0")


	button_widget = Button(tk, text="Finalize Move")
	button_widget.bind("<Button-1>", lambda e: update_score(e, canvas, button_widget))
	button_widget.pack()
	

	canvas.pack()
	canvas.bind()

	canvas.mainloop()


if __name__ == '__main__':
	main()