""" Message handler class """

import logging as log
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

log.basicConfig(level=log.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
# log.disable(log.INFO)


class Message:
    """ Data class"""
    def __init__(self, user_id, text, event_type):
        self.user_id = user_id
        self.text = text
        self.event_type = event_type

    @property
    def message(self):
        return self.__text__

    @message.setter
    def message(self, message):
        if message is not None and len(message) > 0:
            self.__text__ = message
        else:
            self.__text__ = 'None'


class VkChat:
    """ Message handler class """
    def __init__(self, login=None, password=None, token=None):
        self._login = login
        self._password = password
        self._access_token = token

        self._session = self._build_session()
        self._chat = self._session.get_api()

    def _build_session(self):
        """ initialize vk session """
        if self._access_token is None:
            session = vk_api.VkApi(self._login, self._password)
        else:
            session = vk_api.VkApi(token=self._access_token)

        return session

    def start_polling(self):
        """ Block thread and start polling """
        longpoll = VkLongPoll(self._session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                log.info('Received from id: {}: "{}"'.format(event.user_id, event.text))
                yield Message(event.user_id, event.text, event.type)

            elif event.type == VkEventType.USER_ONLINE and event.from_chat:
                log.info('User in online id: {}'.format(event.user_id))
                yield Message(event.user_id, None, event.type)

            log.debug('Event {}'.format(event.type))

    def send_text(self, user_id, text):
        self._chat.messages.send(
            user_id=user_id,
            message=text
        )
