import time

from wcferry import Wcf
import xml.etree.ElementTree as ET

from PluginClub.club_command import CommandRules, \
    NewActivityCommand, UpdateActivityCommand, JoinActivityCommand, CheckActivityCommand, HelpCommand,\
    OperateBonus,ConsumeBonus,DonateBonus,QueryBonusBalance,QueryBonusFlow,QueryBonusAll,QueryBalanceAll
from PluginClub.DataBase.club_activity import OutputMessageIterator,CommandHelper
from PluginClub.club_plugin_config import club_config
from WeChatCore.wechat_bot import GLOBAL_WCF, GLOBAL_CONTACTS
from WeChatCore.wechat_message import WeChatMessage

command_list = [
    NewActivityCommand(),
    UpdateActivityCommand(),
    JoinActivityCommand(),
    CheckActivityCommand(),
    HelpCommand(),
    OperateBonus(),
    ConsumeBonus(),
    DonateBonus(),
    QueryBonusBalance(),
    QueryBonusFlow(),
    QueryBonusAll(),
    QueryBalanceAll(),
]


class ClubMessageHandler:
    @staticmethod
    def on_group_message(wcf: Wcf, msg: WeChatMessage):
        room_id = msg.roomid
        sender_id = msg.sender
        # if is not activated group
        if not club_config.is_group_activated(room_id=room_id):
            return
        for command in command_list:
            # if is not a command
            if not command.is_command(msg):
                continue
            # if is not a group allowed command
            if not (command.command_rule & CommandRules.GROUP_MESSAGE_ALLOW):
                continue
            # if it's ad admin allowed command but sender is not an admin
            if command.command_rule & CommandRules.ADMIN_ALLOW and \
                    not club_config.is_account_manager(room_id=room_id, wxid=sender_id):
                continue
            try:
                output_iterator = command.parse_command(msg)
                for new_message in output_iterator:
                    time.sleep(0.2)
                    GLOBAL_WCF.send_text(msg=f"{new_message}", receiver=room_id,
                                     aters=sender_id)
                return
            except Exception as e:
                new_message = str(e)
                time.sleep(0.2)
                GLOBAL_WCF.send_text(msg=f"@{GLOBAL_CONTACTS.wxid2wxname(sender_id)}\n{new_message}", receiver=room_id,
                                     aters=sender_id)
                return

    @staticmethod
    def on_direct_message(wcf: Wcf, msg: WeChatMessage):
        sender_id = msg.sender
        for command in command_list:
            # if is not a command
            if not command.is_command(msg):
                continue
            # if is not a direct allowed command
            if not (command.command_rule & CommandRules.DIRECT_MESSAGE_ALLOW):
                continue
            # if is admin allowed command but sender is not an admin
            if command.command_rule & CommandRules.ADMIN_ALLOW and \
                    not club_config.is_one_of_managers(wxid=sender_id):
                continue
            try:
                output_iterator = command.parse_command(msg)
                for new_message in output_iterator:
                    time.sleep(0.2)
                    GLOBAL_WCF.send_text(msg=new_message, receiver=sender_id)
                return
            except Exception as e:
                new_message = str(e)
                time.sleep(0.2)
                GLOBAL_WCF.send_text(msg=new_message, receiver=sender_id)
    @staticmethod
    def on_friends_invitation(wcf: Wcf, msg: WeChatMessage):
        sender_id = msg.sender
        for command in command_list:
            # if is admin allowed command but sender is not an admin
            # if command.command_rule & CommandRules.ADMIN_ALLOW and \
            #         not club_config.is_one_of_managers(wxid=sender_id): # TODO need config on config.ymal
            #     continue
            try:
                xml = ET.fromstring(msg.content)
                sender_id = xml.attrib["fromusername"]
                v3 = xml.attrib["encryptusername"]
                v4 = xml.attrib["ticket"]
                scene = int(xml.attrib["scene"])
                GLOBAL_WCF.accept_new_friend(v3,v4,scene)
                hello_message = f"欢迎使用机器人"
                time.sleep(0.5)
                GLOBAL_WCF.send_text(msg=hello_message, receiver=sender_id)
                output_iterator = CommandHelper.get_help_message()
                for new_message in output_iterator:
                    GLOBAL_WCF.send_text(msg=new_message, receiver=sender_id)
                return
            except Exception as e:
                new_message = str(e)
                GLOBAL_WCF.LOG.error(f"Friends invitation Error:{e}")
