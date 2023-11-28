import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

def enhanceColor(image:np.ndarray, factor:float, canal:int):

	new_img = image.astype(np.float32)
	
	new_img[:,:,canal] = new_img[:,:,canal]*factor
	new_img = new_img.astype(np.int32)

	return np.clip(new_img, 0, 255)

def imagemMosaico(img:np.ndarray, w:int):
	new_img = np.zeros(img.shape, np.int32)

	d = w//2

	for i in range(d, len(img), w):
		for j in range(d, len(img[0]), w):
			new_img[i-d:i+d+1, j-d:j+d+1] = img[i,j]

	return np.clip(new_img, 0, 255)

def color2gray(imgB:np.ndarray):
	new_img = np.zeros(imgB.shape[:-1], dtype=np.int32)

	height, width = new_img.shape

	for i in range(height):
		for j in range(width):
			r, g, b = imgB[i,j]
			new_img[i][j] = 0.2978*r + 0.5870*g + 0.1140*b

	return np.clip(new_img, 0, 255)

def imagemBin(imgG:np.ndarray, limiar:int):
	imgG[imgG>limiar] = 255
	imgG[imgG<=limiar] = 0

	return imgG

def imagemCont(imgBin:np.ndarray):
	new_img = np.zeros(imgBin.shape, dtype=np.int32)

	height, width = imgBin.shape

	for i in range(height):
		for j in range(width):
			cur = imgBin[i][j]

			new_img[i][j] = not (
				(i-1 >= 0     and cur == imgBin[i-1,j]) and \
				(i+1 < height and cur == imgBin[i+1,j]) and \
				(j-1 >= 0     and cur == imgBin[i,j-1]) and \
				(j+1 < width  and cur == imgBin[i,j+1])
			)

	return new_img


def main():
	file_name = './files/polarbear.jpg'

	img = mpimg.imread(file_name)

	# exe 3
	plt.imshow(img)
	plt.axis('off')
	# plt.show()
	
	# exe 4
	enhanced_img = enhanceColor(img, 2, 2)
	plt.imshow(enhanced_img)
	plt.axis('off')
	# plt.show()
	
	# # exe 5
	# mosaico_img = imagemMosaico(img, 12)
	# plt.imshow(mosaico_img)
	# plt.axis('off')
	# # plt.show()

	# exe 6
	gray_img = color2gray(enhanced_img)
	plt.imshow(gray_img, cmap='gray')
	plt.axis('off')
	# plt.show()

	# exe 7
	bin_img = imagemBin(gray_img, 85)
	plt.imshow(bin_img, cmap='gray')
	plt.axis('off')
	# plt.show()

	# exe 8
	cont_img = imagemCont(bin_img)
	plt.imshow(cont_img, cmap='gray')
	plt.axis('off')
	plt.show()

	# exe 9
	plt.imsave('./ola.bmp', img, cmap='gray')
	


if __name__ == '__main__':
	main()
