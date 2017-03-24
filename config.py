class basic_config(object):
    SECRET_KEY = '1fb6c473ae99b84387f0136d3947def0'


class prod_config(object):
    pass


class dev_config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://apktool:Apktool@2017@localhost/myblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
