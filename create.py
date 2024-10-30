#!/usr/bin/python3

from os import getenv
from requests import get
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

margin = 100
padding = 10
width = 1920
height = 1080
columns = 5
icon_width = 300

i = 0

img = Image.open('backdrop.jpg')

draw = ImageDraw.Draw(img)
font = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 72)

#draw.rectangle([(192, 108), (1920-192, 1080-108)], fill="#000000")

response = get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/49581?apikey={getenv('API_KEY')}&metric=true")

for day in response.json()['DailyForecasts']:
	print(f"{datetime.strptime(day['Date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%a')}:\n\tL: {day['Temperature']['Minimum']['Value']}°C\n\tH: {day['Temperature']['Maximum']['Value']}°C\n\tIcon: {day['Day']['Icon']}")
	draw.rectangle(
		[
			(width - margin * 2) / columns * i + margin + padding,
			margin + padding,
			(width - margin * 2) / columns * (i + 1) + margin - padding,
			height - margin - padding
		],
		fill="#555555",
		outline = "#ffffff")
	draw.text(((width - margin * 2) / columns * (i + 0.5) + margin, 200), datetime.strptime(day['Date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%a') , (255, 255, 255), font = font, anchor = "mm")
	icon = Image.open(f"icons/{str(day['Day']['Icon']).zfill(2)}.png.large")
	img.paste(icon, (int((width - margin * 2) / columns * (i + 0.5) + margin - icon_width / 2), 250), icon)
	i += 1

img.save('test.png')
