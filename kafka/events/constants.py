from enum import Enum


class Events(str, Enum):
    like = 'like'
    pause_movie = 'pause_movie'


class Services(str, Enum):
    movies = 'movies'


def get_topic_name(service: Services, event: Events):
    return f'stream_{service.value}_{event.value}'
