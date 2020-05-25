#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import os
import boto3
import s3fs
import errno
import io
import warnings
import secrets_manager
import json
get_secret = json.loads(secrets_manager.get_secret())
print(get_secret)
key = get_secret.get('key')
secret = get_secret.get('secret')
s3 = s3fs.S3FileSystem(anon = False, key=key, secret=secret)

#fake data
dates = pd.date_range('20130101', periods=6)

df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))

#s3 bucket
bucket = 'pv-capstone-project'
# CSV_files
outname = "sample_test.csv"
outdir = "s3://" + bucket 

#functions
def _write_dataframe_to_csv_on_s32(dataframe, filename):
    """ Write a dataframe to a CSV on S3 """
    print("Writing {} records to {}".format(len(dataframe), filename))
    #########
    bytes_to_write = dataframe.to_csv(None, index = False).encode()
    with s3.open(filename, 'wb') as f:
        f.write(bytes_to_write)
        
def _write_image_on_s3(bucket ,fullname_image):
    ### save image
    canvas = FigureCanvasAgg(fig) # renders figure onto canvas
    imdata = io.BytesIO() # prepares in-memory binary stream buffer (think of this as a txt file but purely in memory)
    canvas.print_png(imdata) # writes canvas object as a png file to the buffer. You can also use print_jpg, alternatively

    image_s3 = boto3.resource('s3') # or whatever region your s3 is in

    image_s3.Object(bucket ,fullname_image).put(Body=imdata.getvalue(),
                                              ContentType='image/png')

fullname = os.path.join(outdir, outname)
_write_dataframe_to_csv_on_s32(df, fullname)





