from core.crud.base import BaseCrud
from models import Event


class EventCrud(BaseCrud):
    pass


event_crud = EventCrud(entity=Event)
