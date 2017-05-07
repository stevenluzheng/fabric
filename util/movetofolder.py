import os
import shutil
import Image
fold = '.'
imgsfiles = [ os.path.join(fold,img) for img in os.listdir(os.path.join(fold))]
i = 0
for imgsfile in imgsfiles:
   if 'jpg' in imgsfile:
    im = Image.open(imgsfile)
    width, height = im.size
    if width >300:	
      fold = imgsfile.split('.jpg')[0]
      os.mkdir(fold)
      fn = os.path.basename(fold)	  
      dst = os.path.join(fold,fn+'.jpg')	  
      shutil.move(imgsfile,dst)	
