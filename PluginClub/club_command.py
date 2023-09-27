import re
from datetime import datetime

from PluginClub.DataBase.club_activity import ClubActivityManager
from WeChatCore.wechat_bot import GLOBAL_CONTACTS, GLOBAL_ROOMS
from WeChatCore.wechat_message import WeChatMessage


class CommandRules:
    GROUP_MESSAGE_ALLOW = 0x01
    DIRECT_MESSAGE_ALLOW = 0x02
    EVERY_ONE_ALLOW = 0x04
    ADMIN_ALLOW = 0x08


class CommandBase:

    def __init__(self):
        self.command_head: str = ""
        self.command_rule: int = 0x00

    def parse_command(self, msg: WeChatMessage):
        raise NotImplementedError

    def is_command(self, msg: WeChatMessage):
        content = msg.content.lstrip()
        return content.startswith(self.command_head)

    @staticmethod
    def _parse_date_str(date_str: str):
        try:
            date_ = date_str.split("-")
            date_result = datetime(year=int(date_[0]), month=int(date_[1]), day=int(date_[2]))
            return date_result
        except Exception as e:
            raise Exception("Error in Date Parsing")

    @staticmethod
    def _extract_from_pattern(content: str, pattern: str, is_optional: bool = False) -> str:
        """
        should only have one group
        :param content:
        :param pattern:
        :param is_optional: when extraction failed if it's optional , will directly return empty
        :return:
        """
        result = re.findall(pattern=pattern, string=content)
        if len(result) <= 0:
            error = f"Didn't matched pattern {pattern}"
            if is_optional:
                return ""
            raise Exception(error)
        return result[0]


class ActivityCommandBase(CommandBase):
    # activity management
    TITLE_PATTERN = r"活动名称.*\[(.*)\]"
    START_DATE_PATTERN = r"活动开始时间.*\[(.*)\]"
    END_DATE_PATTERN = r"活动结束时间.*\[(.*)\]"
    PLACE_PATTERN = r"活动地点.*\[(.*)\]"
    PLANED_PEOPLE_PATTERN = r"活动人数限制.*\[(.*)\]"
    POINT_BUDGET_PATTERN = r"活动积分预算.*\[(.*)\]"
    POINT_PATTERN = r"单次参与/打卡积分奖励.*\[(.*)\]"
    MAX_EARN_COUNT = r"最大积分打卡次数.*\[(.*)\]"

    # activity participant
    JOINED_REAL_NAME_PATTERN = r"参与人.*\[(.*)\]"

    def __init__(self):
        super().__init__()

    def _parse_activity_start_datetime(self, string: str):
        start_date_str = self._extract_from_pattern(content=string, pattern=self.START_DATE_PATTERN)
        return self._parse_date_str(start_date_str)

    def _parse_activity_end_datetime(self, string: str):
        start_date_str = self._extract_from_pattern(content=string, pattern=self.END_DATE_PATTERN)
        end_date = self._parse_date_str(start_date_str)
        end_date = datetime(year=end_date.year, month=end_date.month, day=end_date.day,
                            hour=23, minute=59, second=59)
        return end_date


class NewActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".发起活动"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | CommandRules.ADMIN_ALLOW

    def parse_command(self, msg: WeChatMessage):
        room_id = msg.roomid
        room_name = GLOBAL_ROOMS.from_room_id_to_room_name(room_id)
        title = self._extract_from_pattern(content=msg.content, pattern=self.TITLE_PATTERN)
        full_content = str(msg.content).replace(self.command_head, "").lstrip()
        organizer_id = msg.sender
        organizer_name = GLOBAL_CONTACTS.wxid2wxname(organizer_id)
        start_date = self._parse_activity_start_datetime(msg.content)
        end_date = self._parse_activity_end_datetime(msg.content)

        # for all optional information
        place = self._extract_from_pattern(content=msg.content, pattern=self.PLACE_PATTERN, is_optional=True)
        planed_people = self._extract_from_pattern(content=msg.content, pattern=self.PLANED_PEOPLE_PATTERN,
                                                   is_optional=True)
        point_budget = self._extract_from_pattern(content=msg.content, pattern=self.POINT_BUDGET_PATTERN,
                                                  is_optional=True)
        point = self._extract_from_pattern(content=msg.content, pattern=self.POINT_PATTERN, is_optional=True)
        max_earn_count = self._extract_from_pattern(content=msg.content, pattern=self.MAX_EARN_COUNT, is_optional=True)

        return ClubActivityManager.new_activity(room_id=room_id,
                                                room_name=room_name,
                                                title=title,
                                                full_content=full_content,
                                                organizer_id=organizer_id,
                                                organizer_name=organizer_name,
                                                start_date=start_date,
                                                end_date=end_date,
                                                place=place,
                                                planed_people=planed_people,
                                                point_budget=point_budget,
                                                point=point,
                                                max_earn_count=max_earn_count,
                                                )


class UpdateActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".更新活动"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | CommandRules.ADMIN_ALLOW

    def parse_command(self, msg: WeChatMessage):
        room_id = msg.roomid
        room_name = GLOBAL_ROOMS.from_room_id_to_room_name(room_id)
        title = self._extract_from_pattern(content=msg.content, pattern=self.TITLE_PATTERN)
        full_content = str(msg.content).replace(self.command_head, "").lstrip()
        organizer_id = msg.sender
        organizer_name = GLOBAL_CONTACTS.wxid2wxname(organizer_id)
        start_date = self._parse_activity_start_datetime(msg.content)
        end_date = self._parse_activity_end_datetime(msg.content)

        # for all optional information
        place = self._extract_from_pattern(content=msg.content, pattern=self.PLACE_PATTERN, is_optional=True)
        planed_people = self._extract_from_pattern(content=msg.content, pattern=self.PLANED_PEOPLE_PATTERN,
                                                   is_optional=True)
        point_budget = self._extract_from_pattern(content=msg.content, pattern=self.POINT_BUDGET_PATTERN,
                                                  is_optional=True)
        point = self._extract_from_pattern(content=msg.content, pattern=self.POINT_PATTERN, is_optional=True)
        max_earn_count = self._extract_from_pattern(content=msg.content, pattern=self.MAX_EARN_COUNT, is_optional=True)
        return ClubActivityManager.update_activity(room_id=room_id,
                                                   room_name=room_name,
                                                   title=title,
                                                   full_content=full_content,
                                                   organizer_id=organizer_id,
                                                   organizer_name=organizer_name,
                                                   start_date=start_date,
                                                   end_date=end_date,
                                                   place=place,
                                                   planed_people=planed_people,
                                                   point_budget=point_budget,
                                                   point=point,
                                                   max_earn_count=max_earn_count,
                                                   )


class CheckActivityCommand(ActivityCommandBase):
    # check the activity record
    def __init__(self):
        super().__init__()
        self.command_head = ".活动状态"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.ADMIN_ALLOW | \
                            CommandRules.DIRECT_MESSAGE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        title = self._extract_from_pattern(content=msg.content, pattern=self.TITLE_PATTERN)
        flag = 0x01 if msg.from_group() else 0x07  # in group show only name, direct show all
        return ClubActivityManager.show_activity_status(title=title, show_flag=flag)


class JoinActivityCommand(ActivityCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".打卡"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        title = self._extract_from_pattern(content=msg.content, pattern=self.TITLE_PATTERN)
        partici_id = msg.sender
        partici_name = GLOBAL_CONTACTS.wxid2wxname(partici_id)
        partici_real_name = self._extract_from_pattern(content=msg.content, pattern=self.JOINED_REAL_NAME_PATTERN)
        content = str(msg.content).replace(self.command_head, "").lstrip()
        return ClubActivityManager.new_participates(title=title,
                                                    partici_id=partici_id,  # TODO can be removed
                                                    partici_name=partici_name,  # TODO can be removed
                                                    partici_real_name=partici_real_name,
                                                    content=content,
                                                    )


class BonusCommandBase(CommandBase):
    CLUB_NAME_PATTERN = r"俱乐部群名.*\[(.*)\]"
    JOINED_REAL_NAME_PATTERN = r"姓名.*\[(.*)\]"  # multiply query target supported

    def __init__(self):
        super().__init__()


class OperateBonus(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".操作积分"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.ADMIN_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


class ConsumeBonus(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".消费积分"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


class DonateBonus(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".捐献积分"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


class QueryBonusBalance(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".查询积分余额"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


class QueryBonusFlow(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".查询积分流水"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


class QueryBonusAll(BonusCommandBase):
    def __init__(self):
        super().__init__()
        self.command_head = ".查询积分总榜"
        self.command_rule = CommandRules.GROUP_MESSAGE_ALLOW | \
                            CommandRules.EVERY_ONE_ALLOW

    def parse_command(self, msg: WeChatMessage):
        ...


if __name__ == "__main__":
    ...
#     import PluginClub.DataBase.club_db as db
#     import wcferry
#
#     db.table.create_tables()
#     wcf = wcferry.Wcf()
#     GLOBAL_ROOMS = WeChatRooms(wcf=wcf)
#     GLOBAL_CONTACTS = WeChatContacts(wcf=wcf)
#
#     msg = WeChatMessage(msg=wcferry.wcf_pb2.WxMsg())
#     msg.roomid = "44@chatroom"
#     msg.content="""
#     .发起活动
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-11]
#     任意内容
#     """
#     msg.sender = "wx"
#     print(NewActivityCommand().is_command(msg))
#     result = NewActivityCommand().parse_command(msg)
#
#     msg.content="""
#     .更新活动
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-13]
#     任意内容111
#     """
#     if UpdateActivityCommand().is_command(msg):
#         result = UpdateActivityCommand().parse_command(msg)
#     msg.content="""
#     .打卡
#     活动名称: [测试活动1]
#     活动开始时间: [2023-08-08]
#     活动结束时间: [2023-08-13]
#     任意内容111
#     """
#     if JoinActivityCommand().is_command(msg):
#         result = JoinActivityCommand().parse_command(msg)
#         ...
#     ...
#
