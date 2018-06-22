""" Dialogflow v1 api """

import uuid
import json
import requests
import apiai
import logging as log

log.basicConfig(level=log.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
# log.disable(log.INFO)


class DialogFlow:
    def __init__(self, project_id, token):
        self._project_id = project_id
        self._access_token = token

    def text_request(self, message, session_id, lang='ru'):
        """ Send text request to Dialogflow api """
        request = apiai.ApiAI(self._access_token, session_id).text_request()
        request.lang = lang
        request.query = message

        return self._response_text(request.getresponse().read())

    def _response_text(self, data):
        response_json = json.loads(data.decode('utf-8'))
        return response_json['result']['fulfillment']['speech']
