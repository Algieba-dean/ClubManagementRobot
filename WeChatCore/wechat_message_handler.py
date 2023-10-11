from wcferry import Wcf

from WeChatCore.wechat_message import WeChatMessage
import xml.etree.ElementTree as ET


class WeChatMessageHandler:
    def __init__(self):
        self._normal_group_message_handler = list()
        self._direct_message_handler = list()
        self._friends_invitation_handler = list()

    def register_normal_group_message_handler(self, func):
        self._normal_group_message_handler.append(func)

    def register_direct_message_handler(self, func):
        self._direct_message_handler.append(func)
    def register_friends_invitation_handler(self, func):
        self._friends_invitation_handler.append(func)

    def on_message(self, wcf: Wcf, msg: WeChatMessage):
        if msg.from_group():
            # group message handle
            for group_message_handler in self._normal_group_message_handler:
                group_message_handler(wcf, msg)
            return

        if msg.type == 0x01:  # text message
            for direct_message_handler in self._direct_message_handler:
                direct_message_handler(wcf, msg)
        if msg.type == 37: # auto accept friends
            for friends_invitation_handler in self._friends_invitation_handler:
                friends_invitation_handler(wcf,msg)

