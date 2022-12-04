from enum import Enum


class Events(str, Enum):
    like = 'like'
    pause_movie = 'pause_movie'


def get_topic_name(event: Events):
    return f'stream_{event.value}'
