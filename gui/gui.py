from tkinter import *
from pathlib import Path

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

		room_dict = self.parse_room(filename)
		self.canvas = canvas
		self.filename = filename
		self.type = room_dict.get('type')
		self.size = room_dict.get('size')
		self.points = room_dict.get('points')
		self.connections = {
			"type": room_dict["connections"]
		}
		self.rotation = room_dict["rotation"]
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/filename)
		self.photoimg = self.photoimg.subsample(2)
		canvas.tag_bind(self.photoimg, '<ButtonPress-1>', lambda event: move_image(event, canvas, self))
		# canvas.tag_bind(self.photoimg, '<B1-Motion>', move_image)
		canvas.create_image(900*position/7, 900*5/7, anchor=CENTER, image=self.photoimg)


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

	def move_image(self, e, canvas):
		# Needed to reset image position
		self.photoimg = self.photoimg.subsample(1)
		canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)

	def rotate_img(self, e, canvas, room_obj):
		self.rotation = (self.rotation + 90) % 360
		self.filename = self.filename.split('r')[0] + "r" + str(self.rotation).zfill(3) + ".png"
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/self.filename)
		self.photoimg = self.photoimg.subsample(2)
		canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)

		

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
	Sleeping_Room_Test = Room("Ss300p3c2tSr000.png", canvas, 1)
	Outdoor_Room_Test = Room("Os500p4c1tOr000.png", canvas, 2)



	button_widget = Button(tk, text="Finalize Move")
	button_widget.pack()

	canvas.pack()

	# canvas.bind('<B1-Motion>', lambda event: move_image(event, canvas, Sleeping_Room_Test))
	# canvas.bind('<B1-Motion>', lambda event: move_image(event, canvas, Outdoor_Room_Test))
	# canvas.bind('<Double-1>', lambda event: rotate_img(event, canvas, Sleeping_Room_Test))

	canvas.mainloop()


if __name__ == '__main__':
	main()