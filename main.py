import sys
from random import randint

# input_filename = "a_example.txt"
# input_filename = "b_lovely_landscapes.txt"
# input_filename = "c_memorable_moments.txt"
# input_filename = "d_pet_pictures.txt"
input_filename = "e_shiny_selfies.txt"

output_filename = "output_" + input_filename

slides = []

alikes = []
osites = []

def predict(aslide):
	# thres = int(len(aslide[2]) * 0.5) # classification threshold
	thres = 1

	# lthres = int(len(aslide[2]) * 0.1) # low threshold
	lthres = 0 # low threshold
	hthres = int(len(aslide[2]) * 0.1) # high threshold

	for cslide in slides:
		# if it is the same slide then skip it
		if aslide[0] == cslide[0]: continue

		# if it is used then skip it
		if cslide[3] == 0: continue

		# scoring the slide, with counter slide
		a = score(aslide, cslide)

		cslide[3] = 0
		if a < thres:
			# score is very low, similar slides
			# put them as alikes
			if a < lthres:
				alikes.insert(0, cslide)
			else: alikes.append(cslide)
		else:
			# score is very high, counter slides
			# put them as osoites
			if a >= hthres:
				osites.insert(0, cslide)
			else: osites.append(cslide)

def score(slide_one, slide_two):
	stags = slide_one[2] if (len(slide_one[2]) < len(slide_two[2])) else slide_two[2]
	ltags = slide_two[2] if (len(slide_one[2]) < len(slide_two[2])) else slide_one[2]

	a = 0 # a : common
	b = 0 # b : uncommon in stags
	c = 0 # c : uncommon in ltags

	matched = False
	for i in range(len(stags)):
		matched = False
		for j in range(len(ltags)):
			if (stags[i] == ltags[j]):
				a += 1
				matched = True

		if not matched:
			b += 1

	c = len(ltags) - a

	if min(a, b, c) != 0:
		print("score : " + str(slide_one[0]) + " : " + str(slide_two[0]) + " : " + str(a) + ", " + str(b) + ", " + str(c))

	return min(a, b, c)

print("reading input from 'input/" + input_filename +"'")

with open('input/' + input_filename) as input_filetext:
	input_filetext.readline()

	input_slidindex = 0
	for input_fileline in input_filetext:
		input_linesplit = input_fileline.strip().split(" ")

		if len(input_linesplit) > 0:
			input_slide = []
			input_slide_tags = []

			# index 0 : slide id
			input_slide.append(input_slidindex)
			input_slidindex += 1

			# index 1 : slide orientation
			input_slide.append(input_linesplit[0])

			# index 2 : slide tags
			for i in range(int(input_linesplit[1])):
				input_slide_tags.append(input_linesplit[2 + i])
			input_slide.append(input_slide_tags) 

			# index 3 : slide is available or not
			input_slide.append(1)

			# print(input_slide)
			slides.append(input_slide)

print("done : reading input from 'input/" + input_filename +"'")
print()

slideshow = []

# initial_slide = 0
initial_slide = randint(0, len(slides) - 1) 

print("predicting alikes and osits of slide : '" + str(initial_slide) + "'")
# predict all alikes and counters for initial_slide
predict(slides[initial_slide])
print("done : predicting alikes and osites of slide : '" + str(initial_slide) + "'")
print()

# print("alikes : " + str(alikes))
# print("osites : " + str(osites))
# print()

# variable to keep track if current slide is an alike or not
current_alike = True
current_slide = slides[initial_slide]
last_slide = []

# while i have more counters for my current_slide
# then keep on getting the counters until there are none anymore
while True:
	temp_slideshow = []
	next_slide = []

	# if orientation of current slide is vertical
	if "V" in current_slide[1]:
		if not current_alike:
			# then the current vertical is osite, so get another one from there
			for temp_slide in osites:
				if "V" in temp_slide[1]:
					next_slide = temp_slide
			
			if len(next_slide) > 0:
				osites.remove(next_slide)
		else:
			# then the current vertical is alike, so get another one from there
			for temp_slide in alikes:
				if "V" in temp_slide[1]:
					next_slide = temp_slide

			if len(next_slide) > 0:
				alikes.remove(next_slide)

		temp_slideshow.append(current_slide[0])

		# if no next slide was found, break
		last_slide = current_slide
		current_slide = next_slide
		next_slide = []

		if len(current_slide) == 0: break

	try:
		if not current_alike:
			# then the next transition must be opposite, so get an alike
			next_slide = alikes[0]
			
			if len(next_slide) > 0:
				del alikes[0]
		else:
			# then the next transition must be opposite, so get an osite
			next_slide = osites[0]

			if len(next_slide) > 0:
				del osites[0]

		temp_slideshow.append(current_slide[0])
		slideshow.append(temp_slideshow)

		current_alike = not current_alike

		last_slide = current_slide
		current_slide = next_slide
		next_slide = []
	except:
		temp_slideshow.append(current_slide[0])
		slideshow.append(temp_slideshow)

		break

with open(output_filename, "w") as output_filetext:
	print(len(slideshow))
	output_filetext.write(str(len(slideshow)) + "\n")

	for slideshow_slide in slideshow:
		for slideshow_item in slideshow_slide:
			print(slideshow_item, end=" ")
			output_filetext.write(str(slideshow_item) + " ")

		print()
		output_filetext.write("\n")
