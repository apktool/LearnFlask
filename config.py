class basic_config(object):
    pass


class prod_config(object):
    pass


class dev_config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://apktool:Apktool@2017@localhost/myblog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
