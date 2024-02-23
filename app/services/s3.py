import boto3


def initialze_s3():
    session = boto3.Session()
    s3 = session.resource('s3')

    return s3
