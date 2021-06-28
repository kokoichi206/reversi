offset = 20
width = 50
total = 440
cut_off = 0.01
with open('./button_layout.txt', mode='w') as f:
	f.write("# File name: click.py\n")
	text0 = f'<Button>\n'
	text = "\t" + "font_size:  20\n"
	# text1 = "\t" + "color:  0,0,0,0\n"
	font_name = "\t" + "font_name: 'ipag.ttf'\n"
	text1 = "\t" + "color:  0,1,0,1\n"
	text2 = "\t" + "size_hint:  0.11, 0.11\n"
	f.write(text0 + font_name + text + text1 + text2)

	f.write("\n")
	f.write("<FloatLayout>\n")
	for i in range(8):
		for j in range(8):
			x = (offset + width * i) / total - cut_off
			y = (offset + width * j) / total - cut_off
	#		text = "\t" + "Button" + f'{i}{j}:' + "\n"
			text = "\t" + "Button:" + "\n"
			id = '\t\t' + f'id: {i}{j}\n'
			text1 = "\t\t" + "text: ''" + "\n"
			text2 = "\t\t" + "pos_hint: {'x':" + str(x) + ", 'y':" + str(y) + "}\n"
			f.write(text + id + text1 + text2)
