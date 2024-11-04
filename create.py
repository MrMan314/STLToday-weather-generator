#!/usr/bin/python3

from os import getenv
from requests import get
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

margin = 182
padding = 10
width = 1920
height = 1080
columns = 5
icon_width = 300
icon_height = 180
corner_radius = 32
margin_top = 250
margin_bottom = 100

i = 0

img = ImageEnhance.Brightness(Image.open('backdrop.jpg')).enhance(.95)
#.filter(ImageFilter.GaussianBlur(5)))
blurred = img.filter(ImageFilter.GaussianBlur(52))

draw = ImageDraw.Draw(img)
title_font = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 96)
font = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 72)
font2 = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 64)
font3 = ImageFont.truetype('Comfortaa-VariableFont_wght.ttf', 26)


draw.text((width / 2, 175), 'STL 5-Day Weather Forecast' , (255, 255, 255), font = title_font, anchor = "mm", stroke_width=2)
draw.text((0, height), ' https://github.com/MrMan314/STLToday-weather-generator', (255, 255, 255), font=font3, anchor="ld")

response = get(f"http://dataservice.accuweather.com/forecasts/v1/daily/5day/49581?apikey={getenv('API_KEY')}&metric=true")

for day in response.json()['DailyForecasts']:
	print(f"{datetime.strptime(day['Date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%a')}:\n\tL: {day['Temperature']['Minimum']['Value']}°C\n\tH: {day['Temperature']['Maximum']['Value']}°C\n\tIcon: {day['Day']['Icon']}")
	mask = Image.new('L', img.size, 0)
	draw_mask = ImageDraw.Draw(mask)
	x0 = (width - margin * 2) / columns * i + margin + padding
	y0 = margin_top + padding
	x1 = (width - margin * 2) / columns * (i + 1) + margin - padding
	y1 = height - margin_bottom - padding

	draw_mask.rectangle([x0 + corner_radius, y0, x1 - corner_radius, y1], fill="white")
	draw_mask.rectangle([x0, y0 + corner_radius, x1, y1 - corner_radius], fill="white")
	draw_mask.ellipse([x0, y0, x0 + 2 * corner_radius, y0 + 2 * corner_radius], fill="white")
	draw_mask.ellipse([x0, y1 - 2 * corner_radius, x0 + 2 * corner_radius, y1], fill="white")
	draw_mask.ellipse([x1 - 2 * corner_radius, y0, x1, y0 + 2 * corner_radius], fill="white")
	draw_mask.ellipse([x1 - 2 * corner_radius, y1 - 2 * corner_radius, x1, y1], fill="white")

	img.paste(blurred, mask=mask)
	draw.text(((width - margin * 2) / columns * (i + 0.5) + margin, 350), datetime.strptime(day['Date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%a') , (255, 255, 255), font = font, anchor = "mm")
	draw.text(((width - margin * 2) / columns * (i + 0.5) + margin, height - 300), f"H: {round(day['Temperature']['Maximum']['Value'])}°C", (255, 171, 171), font = font2, anchor = "mm")
	draw.text(((width - margin * 2) / columns * (i + 0.5) + margin, height - 200), f"L: {round(day['Temperature']['Minimum']['Value'])}°C", (117, 225, 255), font = font2, anchor = "mm")
	icon = Image.open(f"icons/{str(day['Day']['Icon']).zfill(2)}.png.large")
	img.paste(icon, (int((width - margin * 2) / columns * (i + 0.5) + margin - icon_width / 2), int((height - icon_height + (font.size - font2.size)/2 + 50) / 2)), icon)
	i += 1

#draw.rectangle([(192, 108), (1920-192, 1080-108)], outline="red")

img.save(f'{datetime.now().strftime("%b%d")}_Weather.png')
