from PIL import Image, ImageDraw, ImageFont

img = Image.open('backdrop.jpg')

draw = ImageDraw.Draw(img)
font = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 72)

days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri']

draw.rectangle([(192, 108), (1920-192, 1080-108)], fill="#000000")

margin = 100
padding = 10
width = 1920
height = 1080
columns = 5

for i in range(columns):
	draw.rectangle(
		[
			(width - margin * 2) / columns * i + margin + padding,
			margin + padding,
			(width - margin * 2) / columns * (i + 1) + margin - padding,
			height - margin - padding
		],
		fill="#555555",
		outline = "#ffffff")
	draw.text(((width - margin * 2) / columns * (i + 0.5) + margin, 200), days[i], (255, 255, 255), font = font, anchor = "mm")

img.save('test.png')
