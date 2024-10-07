import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ready-for-open-source')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://') # or \
        # 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/uploads")
    AWS_S3_REGION = 'us-east-1'
    AWS_S3_BUCKET = 'phl-storage-bucket'
    ALLOWED_EXTENSIONS = ['xml', 'mxl']