#!/bin/usr/python
import os
import argparse
import boto3

from os import listdir
from os.path import isfile, join, getctime

from datetime import datetime

def get_files(path):
    files = []
    for file in listdir(path):
        filepath = join(path, file)
        if isfile(filepath):
            files.append({
                'path': filepath,
                'name': file,
                'last_modified': datetime.fromtimestamp(getctime(filepath)).strftime("%Y-%m-%dT%H:%M:%S"),
            })
    return files

def upload_files_to_s3(bucket, prefix, files):
    s3 = boto3.resource('s3')

    failed_uploads = []
    i = 1
    for file in files:
        print('Uploading file {} of {}.'.format(i, len(files)))
        try:
            key = '{}/{}'.format(prefix, file['name'])
            s3.meta.client.upload_file(file['path'], bucket, key, ExtraArgs={
                'Metadata': {
                    'last-modified': file['last_modified']
                }
            })
        except Exception as e:
            file['error'] = str(e)
            failed_uploads.append(file)
        finally:
            i = i + 1
    return failed_uploads

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload video files to Amazon S3.')
    parser.add_argument('path', help='path to folder containing videos')
    parser.add_argument('bucket', help='bucket name')
    parser.add_argument('prefix', help='folder under the bucket')
    args = parser.parse_args()

    files = get_files(args.path)
    print('Found {} files'.format(len(files)))

    failed_uploads = upload_files_to_s3(args.bucket, args.prefix, files)

    if failed_uploads:
        print('Errors were encountered uploading the following objects. Attempting to retry: {}'.format(failed_uploads))
        failed_uploads = upload_files_to_s3(args.bucket, args.prefix, failed_uploads)

        if failed_uploads:
            print('Second attempt to upload files failed for the following: {}'.format(failed_uploads))