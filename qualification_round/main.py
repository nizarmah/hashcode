import sys
from os import path

import re

book_scores = []
all_shipped_books = []

class Library(object):
	library_id = 0
	def __init__(self, num_books, signup, ship):
		self.id = Library.library_id
		Library.library_id += 1

		self.num_books = int(num_books)
		self.signup = int(signup)
		self.ship = int(ship)

		self.books = []

	def add_books(self, books):
		self.books = [ int(book_id) for book_id in books ]

	def added_books(self):
		return (len(self.books) > 0)

	def set_days_left_after_signup(self, days):
		self.days_left = days - self.signup

	def num_shipped_books(self):
		self.num_shipped_books = ((self.days_left + 1) * self.ship)

		if (self.num_shipped_books > self.num_books):
			self.num_shipped_books = self.num_books

		return self.num_shipped_books

	def ship_books(self):
		global all_shipped_books

		sorted_books = sorted(self.books, reverse=True, 
								key=lambda bid : book_scores[bid])

		none_duped_books = sorted(sorted_books, reverse=False,
								key=lambda bid : (bid in all_shipped_books))

		self.shipped_books = none_duped_books[:self.num_shipped_books()]

	def __str__(self):
		return str(dict(id=self.id, num_books=self.num_books,
						signup=self.signup, ship=self.ship))

	def __repr__(self):
		return str(dict(id=self.id, num_books=self.num_books,
						signup=self.signup, ship=self.ship))

def choose_libraries(libraries, key=lambda i : i.signup, reverse=False):
	return sorted(libraries, key=key, reverse=reverse)

def signup_libraries(libraries, days):
	last_library_index = len(libraries)
	for library_index in range(len(libraries)):
		libraries[library_index].set_days_left_after_signup(days)
		days = libraries[library_index].days_left

		if days <= 0:
			offset = 1 if (days == 0) else 0

			last_library_index = library_index + offset
			break

	chosen_libraries = choose_libraries(libraries[:last_library_index], 
										key=lambda i : i.ship, reverse=True)

	return chosen_libraries

def update_shipped_books(libraries):
	global all_shipped_books

	for library_index in range(len(libraries)):
		libraries[library_index].ship_books()

		all_shipped_books += libraries[library_index].shipped_books

def scan_libraries(input_file):
	num_books = -1
	global book_scores

	num_libraries = -1
	libraries = []

	num_days = -1

	with open(input_file) as file:
		for line in file.readlines():
			input_data = line.split()

			if len(input_data) > 0:
				if (num_books == -1) \
						or (num_libraries == -1) \
						or (num_days == -1):
					num_books = int(input_data[0])
					num_libraries = int(input_data[1])
					num_days = int(input_data[2])
				elif len(book_scores) == 0:
					book_scores = [ int(data) for data in input_data ]
				else:
					if (len(libraries) == 0) \
							or libraries[-1].added_books():
						library = Library(input_data[0], 
											input_data[1],
											input_data[2])

						libraries.append(library)
					else:
						libraries[-1].add_books(input_data)

	chosen_libraries = choose_libraries(libraries)

	signedup_libraries = signup_libraries(libraries, num_days)

	print("Number of Days Available: ", num_days)
	print("Signed Up Libraries : ", signedup_libraries)

	update_shipped_books(signedup_libraries)

	input_filename = path.splitext(path.basename(input_file))[0]
	output_file = 'output/' + input_filename + '.out'
	with open(output_file, 'w+') as file:
		num_signedup_libraries = str(len(signedup_libraries))

		print(num_signedup_libraries)
		file.write(num_signedup_libraries)

		for library in signedup_libraries:
			library_info = str(library.id) + ' ' + str(library.num_shipped_books)
			library_books = ' '.join([ str(book_id) 
										for book_id in library.shipped_books ])

			print(library_info)
			file.write('\n' + library_info)

			print(library_books)
			file.write('\n' + library_books)

if __name__ == '__main__':
	scan_libraries(sys.argv[1])
	try:
		pass
	except:
		print('Error : Missing Input File Path')
		print('Usage : python ', path.basename(__file__), ' file.in')