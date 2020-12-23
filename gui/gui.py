from tkinter import *
from pathlib import Path
import time
import os

class Room:
	def __init__(self, filename, position, board, rooms, all_rooms):
		# Create attributes of Room class
		self.filename = filename
		self.board = board
		self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/filename).subsample(3)
		self.room_info = all_rooms[filename[:-9]]
		self.size = self.room_info["size"]
		self.rooms = rooms
		self.points = self.room_info["points"]
		self.dimensions = self.get_dimensions()
		# print("dimensions: " + str(self.dimensions))

		# Set current position of image
		
		if position == 0:
			print("foyer coords")
			self.x_pos = board.width_/2
			self.y_pos = board.height_/2.5
			print("(" + str(self.x_pos) + ", " + str(self.y_pos) + ")")

		else:
			self.x_pos = board.width_*position/8
			self.y_pos = board.height_*6/7
		self.false_x_pos = self.x_pos
		self.false_y_pos = self.y_pos

		# Display image
		self.room_img = board.canvas.create_image(self.x_pos, self.y_pos, anchor=CENTER, image=self.photoimg)
		self.rooms[self.room_img] = self
		
		self.entrances = self.get_entrance_locations()
		self.all_rooms = all_rooms

		self.all_rooms[self.room_img] = self.room_info
		print(self.filename + ": " + str(self.room_img))

		

		# Bind image to double-click and drag/drop events
		self.bind()
		self.move_flag = False
		self.lock = False

	def get_dimensions(self):
		if self.size == 100:
			return (1, 1)
		elif self.size in [125, 150]:
			return (1.5, 1.5)
		elif self.size == 200:
			return (2, 1)
		elif self.size == 250:
			return (2.5, 1)
		elif self.size in [300, 400]:
			return (2, 2)
		elif self.size == 350:
			return (3.5, 1)
		elif self.size == 450:
			return (3, 1.5)
		elif self.size == 500:
			return (2.5, 2.5)
		elif self.size == 600:
			return (3.5, 2)

	def bind(self):
		self.board.canvas.tag_bind(self.room_img, '<Double-1>', lambda x, e = self.room_img: self.rotate_img(x))
		self.board.canvas.tag_bind(self.room_img, '<ButtonRelease-1>', lambda x, e = self.room_img: self.release_img(x))
		self.board.canvas.tag_bind(self.room_img, '<B1-Motion>', lambda x, e = self.room_img: self.move_img(x))

	def release_img(self, e):
		self.move_flag = False

	def move_img(self, e):
		if not self.lock:
			if self.move_flag:
				self.board.canvas.move(self.room_img, e.x-self.false_x_pos, e.y-self.false_y_pos)
			else:
				self.move_flag = True
				self.board.canvas.tag_raise(self.room_img)
		
			self.x_pos = self.photoimg.width()/2 + self.board.canvas.coords(self.room_img)[0]
			self.y_pos = self.photoimg.height()/2 + self.board.canvas.coords(self.room_img)[1] - 60
			self.false_x_pos = e.x
			self.false_y_pos = e.y
			self.board.last_selected_room = self

	def rotate_img(self, e):
		if not self.lock:
			del self.rooms[self.room_img]
			rotation = (int(self.filename.split('.')[0][-3:]) + 90) % 360
			self.filename = self.filename.split('.')[0][:-3] + str(rotation).zfill(3) + ".png"
			self.photoimg = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"rooms"/self.filename)
			self.photoimg = self.photoimg.subsample(3)
			self.room_img = self.board.canvas.create_image(e.x, e.y, anchor=CENTER, image=self.photoimg)
			self.rooms[self.room_img] = self
			print(self.filename + ": " + str(self.room_img))
			# Rebind so object can be rotated again
			self.bind()
			self.board.last_selected_room = self

	def get_entrance_locations(self):
		# Entrances formatted as (<run from center>, <rise from center>)
		
		plot_entrances = {
			"lateral": [],
			"vertical": []
		}

		# left edge
		plot_entrances["lateral"].extend(self.get_lateral_entrances("left"))

		# top edge
		plot_entrances["vertical"].extend(self.get_lateral_entrances("top"))

		# right edge
		plot_entrances["lateral"].extend(self.get_lateral_entrances("right"))

		# bottom edge
		plot_entrances["vertical"].extend(self.get_lateral_entrances("bottom"))
		return plot_entrances

	def get_lateral_entrances(self, side):
		entrance_arr = []
		for entrance in self.room_info["entrances"][side + "_edge"]:
			if entrance == "NA":
				continue

			# x coordinate
			x = 0
			if side == "left":
				x = -self.photoimg.width()/2
			else:
				x = self.photoimg.width()/2
			
			# Find length of ridge of room
			increment = float(self.photoimg.height()/self.dimensions[1]/8)
			deviation = 0
			if (self.dimensions[1]*2) % 2 == 1:
				deviation = increment*4
			else:
				deviation = increment*2

			# y coorindate
			y = 0
			if entrance == "far_top":
				y = -self.photoimg.height()/2 + increment*2
				if self.size == 300 and side == "right":
					x = 0
			elif entrance == "far_bottom":
				y = self.photoimg.height()/2 - increment*2
				if self.room_img == 4:
					print("gallery of mirrors y coord: " + str(y))
			elif entrance == "1_top":
				y = -deviation
				if self.size == 300 and side == "right":
					x = 0
			elif entrance == "2_top":
				y = -deviation - increment*4
				if self.size == 300 and side == "right":
					x = 0
			elif entrance == "1_bottom":
				y = deviation
			elif entrance == "2_bottom":
				y = deviation + increment*4
			elif entrance == "center":
				y = 0
			elif entrance == "NA":
				print("miscalculation with entrance")
				exit(1)

			# add to arr
			entrance_arr.append((x, y))
		return entrance_arr

	def get_vertical_entrances(self, top_or_bottom):
		entrance_arr = []
		for entrance in self.room_info["entrances"][top_or_bottom + "_edge"]:
			if entrance == "NA":
				continue

			# y coordinate
			y = 0
			if top_or_bottom == "top":
				y = -self.photoimg.height()/2
			else:
				y = self.photoimg.height()/2
			
			# Find length of ridge of room
			increment = float(self.photoimg.height()/self.dimensions[1]/8)
			deviation = 0
			if (self.dimensions[0]*2) % 2 == 1:
				deviation = increment*4
			else:
				deviation = increment*2

			# x coorindate
			x = 0
			if entrance == "far_right":
				x = self.photoimg.width()/2 - increment*2
			elif entrance == "far_left":
				x = -self.photoimg.width()/2 + increment*2
			elif entrance == "1_right":
				x = deviation
			elif entrance == "2_right":
				x = deviation + increment*4
			elif entrance == "1_left":
				x = -deviation
			elif entrance == "2_left":
				x = -deviation - increment*4
			elif entrance == "center":
				x = 0
			else:
				print("miscalculation with entrance")
				exit(1)

			# add to arr
			entrance_arr.append((x, y))
		return entrance_arr


class Board:
	def __init__(self, tk, game):
		# Create canvas (board)
		self.tk = tk
		self.game = game
		self.width_ = 1400
		self.height_ = 800
		self.canvas = Canvas(self.tk, width=self.width_, height=self.height_)

		self.label = Label(self.tk, text="")
		self.canvas.bind('<B1-Motion>', self.mouse)
		self.label.pack(side=BOTTOM)
		# Background image
		background = PhotoImage(file=Path(__file__).resolve().parent.parent/"images"/"wood.png")
		background = background.zoom(4).subsample(3)
		# Needed to prevent garbage collection
		self.tk.bg = background
		self.canvas.create_image((0, 0), image=background, anchor="nw")

		# Finalize move button
		self.button_widget = Button(tk, text="Finalize Move")
		self.button_widget.bind("<Button-1>", lambda e: self.update_score(e))
		print("button: " + str(self.button_widget))
		self.button_widget.pack()

		self.score = 0
		self.score_text = self.canvas.create_text(200, 60, fill="darkblue", font="Times 25 italic bold", text="Score: " + str(self.score))
		print("score text: " + str(self.score_text))
		self.last_selected_room = None


	def mouse(self, e):
		self.label.config(text="(" + str(e.x) + ", " + str(e.y) + ")")

	def update_score(self, e):
		self.canvas.delete(self.score_text)
		self.score += int(self.last_selected_room.points)
		# canvas.delete(canvas)
		x = self.last_selected_room.x_pos
		y = self.last_selected_room.y_pos
		print("current coords: (" + str(x) + ", " + str(y) + ")")
		
		print(self.last_selected_room.entrances)
		for entrance in self.last_selected_room.entrances["lateral"]:
			# Create radius for entrance of room just placed
			x1 = x + entrance[0] + 30
			x2 = x + entrance[0] - 30
			y1 = y + entrance[1] + 30
			y2 = y + entrance[1] - 30
			closest_room = self.canvas.find_overlapping(x1, y1, x2, y2)
			print(closest_room)

			# Look at all rooms touching that entrance
			for room in closest_room:
				if room > 1 and room != self.last_selected_room.room_img:
					if self.last_selected_room.room_img == 9:
						print("theater entrance: (" + str(entrance[0]) + ", " + str(entrance[1]) + ")")
					if self.is_connected(x + entrance[0], y + entrance[1], room, "lateral"):
						
						# Check if last_selected_room has points for connections
						connection_info = self.last_selected_room.room_info.get("connections")
						if connection_info:
							for connection_type in connection_info["type"]:
								if self.game.all_rooms[room]["type"] == connection_type:
									self.score += int(connection_info["points"])
					
						# Check if room touching last_selected_room has points for connections
						connected_room_info = self.game.all_rooms[room].get("connections")
						if connected_room_info:
							print(connected_room_info)
							for connection_type in connected_room_info["type"]:
								if self.last_selected_room.room_info.get("type") == connection_type:
									self.score += int(connected_room_info["points"])
			
		self.score_text = self.canvas.create_text(200, 60, fill="darkblue", font="Times 25 italic bold", text="Score: " + str(self.score))

		# print("score text: " + str(self.score_text))

		self.button_widget.bind("<Button-1>", lambda e: self.update_score(e))
		self.last_selected_room.lock = True


	def is_connected(self, x, y, room, direction):
		entrances = self.game.rooms[room].entrances[direction]
		room_x_pos = self.game.rooms[room].x_pos
		room_y_pos = self.game.rooms[room].y_pos
		for entrance in entrances:
			print("entrance of room just placed")
			print("(" + str(x) + ", " + str(y) + ")")
			print("entrance of room you're connecting to")
			print("(" + str(room_x_pos + entrance[0]) + ", " + str(room_y_pos + entrance[1]) + ")")
			if abs(x - (room_x_pos + entrance[0])) <= 40 and abs(y - (room_y_pos + entrance[1])) <= 40:
				print("connected")
				return True
		return False





class Game:
	def __init__(self, tk):
		self.board = Board(tk, self)
		# self.rooms = self.read_in_rooms(room_file)
		self.rooms = {}
		self.all_rooms = {}

		# Read in rooms
		path = Path(__file__).resolve().parent.parent/"notgui"
		for filename in os.listdir(path):
			if filename.endswith(".txt"):
				with open(path/filename, 'r') as txt:
					
					for line in txt.readlines()[1:]:
						attributes = line.split(' ')
						if len(attributes) == 0:
							continue
						attributes[-1] = attributes[-1].strip('\n')
						
						self.all_rooms[attributes[0]] = {
							"filename": attributes[0] + "_r000.png",
							"type": attributes[1],
							"points": attributes[2],
							"num_entrances": attributes[3],
							"connections": {
								"points": attributes[4],
								"type": attributes[6].split(',')
							},
							"entrances": {
								"left_edge": attributes[7].split(','),
								"top_edge": attributes[8].split(','),
								"right_edge": attributes[9].split(','),
								"bottom_edge": attributes[10].split(',')
							},
							"size": int(filename[:-4])
						}

	
		# Read in foyers
		temp_arr = ["yellow", "blue", "red", "green"]
		for val in temp_arr:
			self.all_rooms[val + "_foyer"] = {
				"filename": val + "_foyer_r000.png",
				"type": "corridor",
				"points": 0,
				"num_entrances": 3,
				"connections": None,
				"entrances": {
					"left_edge": ["center"],
					"top_edge": ["center"],
					"right_edge": ["center"],
					"bottom_edge": ["NA"]
				},
				"size": 125
			}
		
		# Read in hallway
		self.all_rooms["hallway"] = {
			"filename": "hallway_r000.png",
			"type": "corridor",
			"points": 0,
			"num_entrances": 14,
			"connections": None,
			"entrances": {
				"left_edge": ["center"],
				"top_edge": ["far_left", "2_left", "1_left", "center", "1_right", "2_right", "far_right"],
				"right_edge": ["center"],
				"bottom_edge": ["far_left", "2_left", "1_left", "center", "1_right", "2_right", "far_right"],
			},
			"size": 150
		}

		# Read in stairway
		self.all_rooms["stairs"] = {
			"filename": "stairs_r000.png",
			"type": "corridor",
			"points": 0,
			"num_entrances": 2,
			"connections": None,
			"entrances": {
				"left_edge": ["center"],
				"top_edge": ["NA"],
				"right_edge": ["center"],
				"bottom_edge": ["NA"],
			},
			"size": 75
		}

		Room("yellow_foyer_r000.png", 0, self.board, self.rooms, self.all_rooms)
		self.draw_rooms()

	def read_in_rooms(self, room_file):
		# Read in rooms from txt file and
		# create room objects
		return 0

	def draw_rooms(self):
		# Pick random rooms one at a time
		# until 7 rooms are displayed
		Room("gallery_of_mirrors_r000.png", 1, self.board, self.rooms, self.all_rooms)
		Room("hundings_hut_r000.png", 2, self.board, self.rooms, self.all_rooms)
		Room("broom_closet_r000.png", 3, self.board, self.rooms, self.all_rooms)
		Room("the_hole_r000.png", 4, self.board, self.rooms, self.all_rooms)
		Room("drawing_room_r000.png", 5, self.board, self.rooms, self.all_rooms)
		Room("theater_r000.png", 6, self.board, self.rooms, self.all_rooms)
		Room("nap_room_r000.png", 7, self.board, self.rooms, self.all_rooms)


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