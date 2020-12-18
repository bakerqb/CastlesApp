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
		# Filename = Ss300p3c2tSr270
		# <type of room> (S for sleeping)
		# s<size>
		# p<points>
		# c<points for connection>
		# t<type of room connection>
		# (c and t won't exist if there are no room connections)
		# r<rotation angle> 

		
		self.canvas = canvas
		self.filename = filename
		
		'''
		room_dict = self.parse_room(filename)
		self.type = room_dict.get('type')
		self.size = room_dict.get('size')
		self.points = room_dict.get('points')
		self.connections = {
			"type": room_dict["connections"]
		}
		'''
		self.rotation = 0
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/filename)
		self.photoimg = self.photoimg.subsample(2)
		
		# canvas.tag_bind(self.photoimg, '<ButtonPress-1>', move_image)
		self.room_img = canvas.create_image(900*position/7, 900*5/7, anchor=CENTER, image=self.photoimg)
		
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

	def rotate_img(self, e):
		self.rotation = (self.rotation + 90) % 360
		self.filename = self.filename.split('.')[0][:-3] + str(self.rotation).zfill(3) + ".png"
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/self.filename)
		self.photoimg = self.photoimg.subsample(2)
		self.room_img = self.canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)
		self.bind()
		self.canvas.pack()


def refresh(canvas):
	while True:
		canvas.update()
		time.sleep(0.01)	


def main():
	width_ = 900
	height_ = 900

	tk = Tk()
	canvas = Canvas(tk, width=width_, height=height_)

	foyer = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/"yellowFoyer.png")
	foyer = foyer.subsample(2)
	canvas.create_image(width_/2, height_/2, anchor=CENTER, image=foyer)

	global Sleeping_Room_Test
	global Outdoor_Room_Test
	Sleeping_Room_Test = Room("queens_bedroom_r000.png", canvas, 1)
	Outdoor_Room_Test = Room("hundings_hut_r000.png", canvas, 2)



	button_widget = Button(tk, text="Finalize Move")
	button_widget.pack()

	canvas.pack()
	# canvas.bind('<B1-Motion>', lambda event: move_image(event, canvas, Sleeping_Room_Test))
	# canvas.bind('<B1-Motion>', lambda event: move_image(event, canvas, Outdoor_Room_Test))
	# canvas.bind('<Double-1>', lambda event: rotate_img(event, canvas, Sleeping_Room_Test))

	# refresh_thread = threading.Thread(target=refresh, args=(canvas))
	# refresh_thread.start()

	canvas.mainloop()
	# refresh_thread.join()


if __name__ == '__main__':
	main()