from tkinter import *
from pathlib import Path
import time

class Room:
	def __init__(self, filename, position, board):
		# Create attributes of Room class
		self.filename = filename
		self.board = board
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/filename).subsample(3)

		# Set current position of image
		if position == 0:
			self.x_pos = board.width_/2
			self.y_pos = board.height_/2.5
		else:
			self.x_pos = board.width_*position/8
			self.y_pos = board.height_*6/7

		# Display image
		self.room_img = board.canvas.create_image(self.x_pos, self.y_pos, anchor=CENTER, image=self.photoimg)

		# Bind image to double-click and drag/drop events
		self.bind()
		self.move_flag = False


	def bind(self):
		self.board.canvas.tag_bind(self.room_img, '<Double-1>', lambda x, e = self.room_img: self.rotate_img(x))
		self.board.canvas.tag_bind(self.room_img, '<ButtonRelease-1>', lambda x, e = self.room_img: self.release_img(x))
		self.board.canvas.tag_bind(self.room_img, '<B1-Motion>', lambda x, e = self.room_img: self.move_img(x))

	def release_img(self, e):
		self.move_flag = False

	def move_img(self, e):
		if self.move_flag:
			self.board.canvas.move(self.room_img, e.x-self.x_pos, e.y-self.y_pos)
		else:
			self.move_flag = True
			self.board.canvas.tag_raise(self.room_img)
		
		self.x_pos = e.x
		self.y_pos = e.y

	def rotate_img(self, e):
		rotation = (int(self.filename.split('.')[0][-3:]) + 90) % 360
		self.filename = self.filename.split('.')[0][:-3] + str(rotation).zfill(3) + ".png"
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/self.filename)
		self.photoimg = self.photoimg.subsample(3)
		self.room_img = self.board.canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)
		
		# Rebind so object can be rotated again
		self.bind()


class Board:
	def __init__(self, tk):
		# Create canvas (board)
		self.tk = tk
		self.width_ = 1400
		self.height_ = 800
		self.canvas = Canvas(self.tk, width=self.width_, height=self.height_)

		# Background image
		background = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"wood.png")
		background = background.zoom(4).subsample(3)
		# Needed to prevent garbage collection
		self.tk.bg = background
		self.canvas.create_image((0, 0), image=background, anchor="nw")

		# Finalize move button
		self.button_widget = Button(tk, text="Finalize Move")
		self.button_widget.bind("<Button-1>", lambda e: self.update_score(e))
		self.button_widget.pack()

		self.score = 0
		self.score_text = self.canvas.create_text(200, 60, fill="darkblue", font="Times 25 italic bold", text="Your score is: " + str(self.score))
	
	def update_score(self, e):
		del self.score_text
		self.score += 1
		self.score_text = self.canvas.create_text(200, 60, fill="darkblue", font="Times 25 italic bold", text="Your score is: " + str(self.score))
		self.button_widget.bind("<Button-1>", lambda e: self.update_score(e))




class Game:
	def __init__(self, tk):
		self.board = Board(tk)
		# self.rooms = self.read_in_rooms(room_file)
		Room("yellow_foyer.png", 0, self.board)
		self.score_text = self.board.canvas.create_text(200, 60, fill="darkblue", font="Times 30 italic bold", text="Your score is: 0")
		self.draw_rooms()

	def read_in_rooms(self, room_file):
		# Read in rooms from txt file and
		# create room objects
		return 0

	def draw_rooms(self):
		# Pick random rooms one at a time
		# until 7 rooms are displayed
		Room("sauna_r000.png", 1, self.board)
		Room("hundings_hut_r000.png", 2, self.board)
		Room("broom_closet_r000.png", 3, self.board)
		Room("the_hole_r000.png", 4, self.board)
		Room("drawing_room_r000.png", 5, self.board)
		Room("theater_r000.png", 6, self.board)
		Room("nap_room_r000.png", 7, self.board)


def main():
	tk = Tk()
	# tk.attributes("-alpha", 0.0)
	g = Game(tk)
	
	# Keep canvas open
	g.board.canvas.pack()
	g.board.canvas.bind()
	# tk.attributes("-transparentcolor", "white")
	g.board.canvas.mainloop()


	
	

	


if __name__ == '__main__':
	main()