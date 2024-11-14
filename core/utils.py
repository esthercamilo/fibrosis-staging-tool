import os
import logging


def create_media_directory():
    media_path = os.path.join(os.getcwd(), 'media')
    if not os.path.exists(media_path):
        os.makedirs(media_path)
        logging.info(f'Diretório {media_path} criado.')
