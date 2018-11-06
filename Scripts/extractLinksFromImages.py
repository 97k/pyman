import pytesseract
import cv2
import re
import numpy as np
from PIL import Image
import sys
from PIL import Image, ImageEnhance, ImageFilter

"""
	Requirements: - pytesseract, Pillow, re
"""

def extractLinks(path_to_image):
	im = Image.open(path_to_image) # the second one 
	im = im.filter(ImageFilter.MedianFilter())
	enhancer = ImageEnhance.Contrast(im)

	im = enhancer.enhance(2)
	im = im.convert('L')

	bw = np.asarray(im).copy()
	# Pixel range is 0...255, 256/2 = 128
	bw[bw < 200] = 35    # Black
	bw[bw > 200] = 25 # White
	imfile = Image.fromarray(bw)
	imfile.save("result_bw.png")

	# im = im.point(lambda x: 0 if x<255 else 150, '1')
	# im.save('temp2.jpg')
	text = pytesseract.image_to_string(Image.open('result_bw.png'))
	print(text)


	text.replace('\n', '')

	text = re.sub('[^a-zA-Z0-9:/ . -]', '', text)

	links = re.findall(r'(https?://\S+)', text)

	import urllib.request
	final_links = []
	for link in links:
		
		try:
			code = urllib.request.urlopen(link).getcode()
			if code!=404:final_links.append(link)
		except HTTPError as e:
			print(link)
			print('error', e)

	return final_links

if __name__ == '__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		print('USAGE: python extractLinksFromImages.py <ImageURL>')
		print('\nExample\n', """python extractLinksFromImages.py ~/Downloads/image.jpeg""")

		exit(1)
	else:
		url = sys.argv[1]

		print('Extracted Links are...\n\n', extractLinks(url))


