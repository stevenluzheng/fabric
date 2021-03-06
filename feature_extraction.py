import numpy as np
import cv2
import mxnet as mx
import argparse
import time
import os
import random
def ch_dev(arg_params, aux_params, ctx):
    new_args = dict()
    new_auxs = dict()
    for k, v in arg_params.items():
        new_args[k] = v.as_in_context(ctx)
    for k, v in aux_params.items():
        new_auxs[k] = v.as_in_context(ctx)
    return new_args, new_auxs
folder = '/home1/slu/work/slu/fabric/10046_samples/'
test_ratio = 0.67
#folder = './imagenet/tiny-imagenet-200/test/images/'
def main():
    synset = [l.strip() for l in open(args.synset).readlines()]
    prefix = "resnet-200"
    num_round = 0	
    model = mx.model.FeedForward.load( prefix, num_round, ctx=mx.gpu(1),numpy_batch_size=1)
    internals = model.symbol.get_internals()
    fea_symbol = internals["fc1_output"]	  
    feature_extractor = mx.model.FeedForward( ctx=mx.gpu(0), symbol=fea_symbol, numpy_batch_size=1, \
            arg_params=model.arg_params, aux_params=model.aux_params, allow_extra_params=True)
			
    subfolders = [ fold for fold in os.listdir(folder)]			
    k = 0	
    for subfolder in subfolders:
      workspace_folder = os.path.join(folder,subfolder)
      print "extract label####",subfolder,k
      i = 0
      k +=1	  
      feature_array = []
      for filename in os.listdir(workspace_folder):
        if '.jpg'	in filename or '.JPEG' in filename:
          i +=1		
          m = cv2.imread(os.path.join(workspace_folder,filename),1)	  
          img = cv2.cvtColor(m, cv2.COLOR_BGR2RGB)
          img = cv2.resize(img, (224, 224))  # resize to 224*224 to fit model
          img = np.swapaxes(img, 0, 2)
          img = np.swapaxes(img, 1, 2)  # change to (c, h,w) order
          img = img[np.newaxis, :]  # extend to (n, c, h, w)
          f = feature_extractor.predict(img)
          #print f.shape		  
          feature_array.append((f[0],subfolder,filename))
      random.shuffle(feature_array)
      #print len(feature_array)	  
      np.save((os.path.join(workspace_folder,"test.npy")),feature_array[:int(i*test_ratio)])
      np.save((os.path.join(workspace_folder,"train.npy")),feature_array[int(i*(test_ratio)):])
	  


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="use pre-trainned resnet model to classify one image")
    parser.add_argument('--img', type=str, default='test.jpg', help='input image for classification')
    parser.add_argument('--gpu', type=int, default=0, help='the gpu id used for predict')
    parser.add_argument('--synset', type=str, default='synset.txt', help='file mapping class id to class name')
    parser.add_argument('--prefix', type=str, default='resnet-200', help='the prefix of the pre-trained model')
    parser.add_argument('--epoch', type=int, default=0, help='the epoch of the pre-trained model')
    args = parser.parse_args()
    main()
