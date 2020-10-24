import os
class Config:
    pass

class ProdConfig(Config):
    '''articles_result = Articles(
                id, author, title, description, url, image, date)
        articles_object.append(articles_result)

    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig

}  