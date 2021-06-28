with open('./below_GridLayout.txt', mode='w') as f:
	init = '          GridLayout:\n'
	c = '               cols: 8\n'
	r = '               rows: 8\n\n'
	f.write(init + c + r)
	
	defo = '               Button:\n'
	defo += '                    size_hint: (.2, .2)\n'
	defo += '                    font_size: 45\n'
	defo += '                    text: ""\n'
	for i in range(8):
		for j in range(8):
			here = f'                    on_press: root.buttonClicked("{i}{j}")\n'
		
			# to make ids
			a = chr(i+97)
			b = chr(j+97)
			ids = f'                    id: {i}{j}\n'
			f.write(defo + here + ids)
	# init = '\t\tGridLayout:\n'
	# c = '\t\t\tcols: 8\n'
	# r = '\t\t\trows: 8\n'
	# f.write(init + c + r)
	
	# defo = '\t\t\tButton:\n'
	# defo += '\t\t\t\tsize_hint: (.2, .2)\n'
	# defo += '\t\t\t\tfont_size: 45\n'
	# defo += '\t\t\t\ttext: ""\n'
	# for i in range(8):
	# 	for j in range(8):
	# 		here = f'\t\t\t\ton_press: root.buttonClicked("{i}{j}")\n'
	# 		f.write(defo + here)
