#django modules
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
#python modules
import string
import boto3
import os
import random

def upload_form_file(file, user_name, save_name):
    '''
    Function to upload private files to S3 Bucket. This returns the url where the file was uploaded.
    :param django-file file: django file to upload
    :param string user_name: username to differentiate the file to the others
    :param string save_name: name of the folder to save the file
    '''
    aws_bucket_name = os.getenv('AWS_PRIVATE_BUCKET_NAME')
    filename, file_extension = os.path.splitext(file.name)
    path = default_storage.save('tmp/file', ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    bucket_file_name = F'{save_name}/{save_name}_{user_name}{file_extension}'
    s3 = boto3.client('s3')
    reponse = s3.upload_file(tmp_file, aws_bucket_name, bucket_file_name, {'ACL': 'public-read',})
    url = F'https://{aws_bucket_name}.s3.amazonaws.com/{bucket_file_name}'
    os.remove(tmp_file)
    return url

def upload_img(file, img_name):
    '''
    Function to upload public images to S3 Bucket. This returns the url to access the picture.
    :param django-file file: django image to upload
    :param string img_name: name of the folder to save the file
    '''
    aws_bucket_name = os.getenv('AWS_PUBLIC_BUCKET_NAME')
    filename, file_extension = os.path.splitext(file.name)
    path = default_storage.save('tmp/file', ContentFile(file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    #create unique string
    letters = string.ascii_letters
    slug = ''.join(random.choice(letters) for i in range(17))
    bucket_file_name = F'{img_name}/{slug}{file_extension}'
    #upload to aws
    s3 = boto3.client('s3')
    reponse = s3.upload_file(tmp_file, aws_bucket_name, bucket_file_name, {'ACL': 'public-read',})
    url = F'https://{aws_bucket_name}.s3.amazonaws.com/{bucket_file_name}'
    os.remove(tmp_file)
    return url


def create_slug(slug_size):
    letters = string.ascii_letters
    slug_ = ''.join(random.choice(letters) for i in range(slug_size))
    return slug_
