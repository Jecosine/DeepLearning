
from PIL import Image
from numpy import *
import pca
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
im=array(Image.open('new1.png').convert('L'))
U,T=pca.denoise(im,im)
Image.fromarray(U).save('denoise.jpg')
Image.fromarray(T).save('noise.jpg')