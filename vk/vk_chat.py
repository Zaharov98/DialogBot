""" Message handler class """

import requests
import logging as log
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

log.basicConfig(level=log.DEBUG, format=" %(asctime)s - %(levelname)s - %(message)s")
# log.disable(log.INFO)


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
            self._handle_vk_event(event)

    def _handle_vk_event(self, event):
        """ handle selected types of events """
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            log.info('Received from id: {}: "{}"'.format(event.user_id, event.text))
            response_text = 'ECHO'

            self._chat.messages.send(
                user_id=event.user_id,
                message=response_text
            )
        elif event.type == VkEventType.USER_ONLINE:
            log.info('User in online id: {}'.format(event.user_id))
            response_text = 'HELLO'

            self._chat.messages.send(
                user_id=event.user_id,
                message=response_text
            )

        log.debug('Event {}'.format(event.type))
