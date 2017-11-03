from pylab import *
from numpy import *
from PIL import Image
'''
mydata = random.rand(256,256)

for i in range(0,256):
	for j in range(0,256):
		mydata[i][j]*=255


figure()

contour(mydata,origin='image')

figure()

hist(mydata.flatten(),128)

show()
'''
img=array(Image.open('new1.jpg').convert('L'))
'''
imshow(img)
x=ginput(3)
print x
show()
'''
#histeq
def histeq(im,nbr_bins=256):
	imhist,bins=histogram(im.flatten(),nbr_bins,normed=True)
	cdf = imhist.cumsum()
	cdf = 255*cdf/cdf[-1]
	im2 = interp(im.flatten(),bins[:-1],cdf)

	return im2.reshape(im.shape),cdf

img2,cdf=histeq(img)
#Image.fromarray(img2).save('img2.jpg')
figure()
gray()
imshow(img2)
figure()
gray()
imshow(img)
figure()
hist(cdf,128)
show()
#imshow(cdf)