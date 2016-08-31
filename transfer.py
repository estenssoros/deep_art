import os
import boto
import progressbar

def aws_keys():
    env = os.environ
    access_key = env['AWS_ACCESS_KEY_ID']
    access_secret_key = env['AWS_SECRET_ACCESS_KEY']
    return access_key, access_secret_key


def connect_s3(bucket_name):
    access_key, access_secret_key = aws_keys()

    conn = boto.connect_s3(access_key, access_secret_key)

    if conn.lookup(bucket_name) is None:
        raise ValueError('Bucket does not exist! WTF!')
    else:
        b = conn.get_bucket(bucket_name)
        print 'Connected to {}!'.format(bucket_name)
    return b


def write_to_s3(fname, directory=None):
    b = connect_s3('sebsimages')

    if directory:
        f = directory + fname

    file_object = b.new_key(f)
    file_object.set_contents_from_filename(f)

    print '{} written to {}!'.format(fname, b.name)


def upload(ext, directory):
    files = [x for x in os.listdir(directory) if x.endswith(ext)]
    b = connect_s3('sebsimages')
    bar = progressbar.ProgressBar()
    for f in bar(files):
        fname = os.path.join(directory,f)
        file_object = b.new_key(fname)
        file_object.set_contents_from_filename(fname)


def download(ext, directory):
    b = connect_s3('sebsimages')
    files = [x for x in b.list(directory) if x.name.endswith(ext)]
    bar = progressbar.ProgressBar()
    for f in bar(files):
        f.get_contents_to_filename(f.name)

def clear_images(directory):
    for f in os.listdir(directory):
        os.remove(os.path.join(directory,f))
    print 'purged from local!'

    b = connect_s3('sebsimages')

    files = [f for f in b.list(directory) if f.name.endswith('.png')]
    bar = progressbar.ProgressBar()
    for f in bar(files):
        f.delete()
    print 'purged from ec2!'

if __name__ == '__main__':
    download('.png','animation')
