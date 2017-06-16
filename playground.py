while True:
	try:
		placement = min(input('Place [{}] at: '.format('X')),6)

		print(placement)
		break
	except NameError:
		print('Please enter a column (0-{})'.format(6))