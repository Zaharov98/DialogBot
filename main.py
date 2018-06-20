""" VK message bot tamplate """

import sys
import json
import logging as log

from vk.vk_chat import VkChat


log.basicConfig(level=log.INFO, format=" %(asctime)s - %(levelname)s - %(message)s")
# log.disable(log.INFO)


def build_config_json(config_path):
    """
    :param config_path: path for config file
    :return json schema dict
    :raise ValueError: if configuration build failed
    """
    try:
        with open(config_path, 'r') as config_file:
            data = json.load(config_file)
            return data
    except Exception as e:
        raise ValueError('Configuration build failed', e)


def main():
    """ App entry point """
    try:
        config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.json'
        config = build_config_json(config_path)

        vk_chat = VkChat(config['vk']['login'], config['vk']['password'], config['vk']['token'])

        log.info('Chat started')
        for message in vk_chat.start_polling():
            log.info('Processing: {}'.format(message.text))

            response = 'ECHO'
            vk_chat.send_message(message.user_id, response)
            log.info('Response: {}'.format(response))

    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    main()
