import os
import boto


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
    file_object.set_contents_from_filename(fname)

    print '{} written to {}!'.format(fname, b.name)


def main():
    write_to_s3('out.png', directory='../neural_artistic_style')


if __name__ == '__main__':
    main()
