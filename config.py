class basic_config(object):
    pass


class prod_config(object):
    pass


class dev_config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:apktool@%:3306/myblog'
