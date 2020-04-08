from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse 




nost = {
	255:	(88, 208, 208),
	172:	(64, 168, 160),
	86:		(40, 128, 112),
	0:		(16, 80, 64)
}

og = {
	255:	255,
	172:	172,
	86:		86,
	0:		0
}

space = {
	255:	(196, 227, 248),
	172:	(149, 52, 204),
	86:		(177, 31, 107),
	0:		(48, 6,11 )
}

cream = {
	255: 	(117, 168, 249),
 	172: 	(211, 246, 255),
  	86: 	(111, 107, 235),
   	0: 		(88, 63, 124)
}


wish = {
	255: (255, 229, 139),
	172: (207, 143, 96),
	86: (232, 80, 117),
	0: (76, 46, 98)
}

aes = {
	255: (218, 242, 241),
	172: (150, 206, 255),
	86: (119, 119, 255),
	0: (59, 48, 0)
}



dictOfDicts = {
	0:	og,
	1:	nost,
	2:	space,
	3:  cream,
	4:  wish,
	5:	aes
}

def hexToBGR(hex):
	lenght = len(hex)
	a,b,c = tuple(int(hex[i:i+lenght//3], 16) for i in range(0, lenght, lenght//3))
	return(c,b,a)


def main():


		
	ap = argparse.ArgumentParser(description='Convert images to GB colours')

	ap.add_argument("-i", "--input", required=True, help="Photo to convert", dest="input")
	ap.add_argument("-o", "--output", required=True, help="Location/name of converted file", dest="output")
	ap.add_argument("-s", "--scale", required=True, type=float, help="Scaling factor", dest="scale")
	ap.add_argument("-p", "--palette", required=False, type=int, help="Palette to choose from", dest="palette")
	ap.add_argument("-c", "--custom", required=False, type=str, help="Use a custom palette", dest="custom", nargs=4)

	args = ap.parse_args()


	im = cv2.imread(args.input,0)

	imgScale = args.scale
	newX = im.shape[1]*imgScale
	newY = im.shape[0]*imgScale
	im = cv2.resize(im,(int(newX),int(newY)))


	img = gbc_filter(im, args.palette, args.custom)

	cv2.imwrite(args.output, img)

def keyway(i,j,sup,range, dic):
	if sup == 255:
		if range == 1:
			return dic[255]
		elif range == 2:
			return dic[255 - ((i%2)*(j%2)*83)]
		elif range == 3:
			return dic[255 - (((j+i+1)%2)*83)]
	elif sup == 172:
		if range == 1:
			return dic[172 + (((i+1)%2)*(j%2)*83)]
		elif range == 2:
			return dic[172]
		elif range == 3:
			return dic[172 - ((i%2)*(j%2)*86)]
		elif range == 4:
			return dic[172 - (((j+i+1)%2)*86)]

	elif sup == 86:
		if range == 1:
			return dic[86 + (((i+1)%2)*(j%2)*86)]
		elif range == 2:
			return dic[86]
		elif range == 3:
			return dic[86 - ((i%2)*(j%2)*86)]
		elif range == 4:
			return dic[ 86 - (((j+i+1)%2)*86)]

	elif sup == 0:
		if range == 1:
			return dic[0 + (((i+1)%2)*(j%2)*86)]
		elif range == 2:
			return dic[0]

def gbc_filter(img, palette, custom):



	if custom == None:
		if palette == None or palette == 0:
			dic = og 
			newImg = img
		else:
			a = np.zeros_like(img)
			newImg = cv2.merge((a,a,a))
			dic = dictOfDicts[palette]
	else:

		dic = {
			255:	hexToBGR(custom[0]),
			172:	hexToBGR(custom[1]),
			86:		hexToBGR(custom[2]),
			0:		hexToBGR(custom[3])
		}

		print(dic)

		a = np.zeros_like(img)
		newImg = cv2.merge((a,a,a))

	for i in range(int(img.shape[0])):
		for j in range(int(img.shape[1])):
			if img[i][j] >= 236:
				newImg[i][j] = keyway(i,j,255,1, dic)
			elif img[i][j] >= 216:
				newImg[i][j] =  keyway(i,j,255,2, dic)
			elif img[i][j] >= 196:
				newImg[i][j] = keyway(i,j,255,3, dic)
			elif img[i][j] >= 176:
				newImg[i][j] = keyway(i,j,172,1, dic)
			elif img[i][j] >= 157:
				newImg[i][j] = keyway(i,j,172,2, dic)
			elif img[i][j] >= 137:
				newImg[i][j] = keyway(i,j,172,3, dic)
			elif img[i][j] >= 117:
				newImg[i][j] = keyway(i,j,172,4, dic)
			elif img[i][j] >= 97:
				newImg[i][j] = keyway(i,j,86,1, dic)
			elif img[i][j] >= 78:
				newImg[i][j] = keyway(i,j,86,2, dic)
			elif img[i][j] >= 58:
				newImg[i][j] = keyway(i,j,86,3, dic)
			elif img[i][j] >= 38:
				newImg[i][j] = keyway(i,j,86,4, dic)
			elif img[i][j] >= 18:
				newImg[i][j] = keyway(i,j,86,1, dic)
			else:
				newImg[i][j] = keyway(i,j,86,1, dic)
	return newImg



if __name__ == '__main__':
	main()