from datetime import datetime

import PluginClub.DataBase.club_db as db
from PluginClub.DataBase import const_var


class OutputMessageIterator:
    def __init__(self):
        self.message_list = list()

    def add_new_message(self, msg: str):
        self.message_list.append(msg)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.message_list) == 0:
            raise StopIteration
        return self.message_list.pop(0)


class CommandHelper:
    USAGE_EXAMPLE = "\n完整使用示例如下:"

    @staticmethod
    def get_help_overview_details() -> str:
        output_message = "\n可用命令如下:\n" \
                         ".发起活动       -- 用于管理员发起活动\n" \
                         ".更新活动       -- 用于管理员更改活动信息\n" \
                         ".活动状态       -- 用于查看活动参与情况\n" \
                         ".打卡          -- 用于参与活动\n" \
                         ".操作积分       -- 用于管理员操作积分\n" \
                         ".消费积分       -- 用于消费积累的积分\n" \
                         ".捐献积分       -- 用于捐赠积分到COMMON用户\n" \
                         ".查询积分余额    -- 用于查询指定用户的积分余额\n" \
                         ".查询积分流水    -- 用于查询指定用户的积分流水\n" \
                         ".查询积分总榜    -- 用于查询累计获得积分的积分榜\n" \
                         ".查询余额总榜    -- 用于查询积分余额的积分榜\n"
        return output_message

    @staticmethod
    def get_help_command_example() -> str:
        example_message = ".帮助" \
                          "\n命令名: [命令]"
        return example_message

    @staticmethod
    def get_new_activity_details() -> str:
        output_message = "\n<.发起活动>\n" \
                         "\n命令类型: [活动命令]" \
                         "\n命令权限: [仅俱乐部管理员可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于管理员发起俱乐部活动, 以发起活动的群名作为俱乐部名称，作为识别俱乐部的唯一标识." \
                         "可设定作为唯一标识的<活动名称>, 设定<活动开始时间><活动结束时间> " \
                         "以及可选设置<活动地点><活动描述><活动人数限制><活动积分预算><单次参与/打卡积分奖励><最大积分打卡次数>等参数]" \
                         "\n\n参数介绍: [" \
                         "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,名称可任意,但是需要保证活动名称唯一)" \
                         "\n\t活动开始时间: [2023-08-01] (必需参数, 日期格式按照范例即可,从当日0点1分1秒开始生效)" \
                         "\n\t活动结束时间: [2023-08-30] (必需参数, 日期格式按照范例即可,截止当日23点59分59秒失效)" \
                         "\n\t活动地点: [线上] (可选参数,可为任意内容) " \
                         "\n\t活动人数限制: [30] (可选参数,非负整数类型" \
                         "不设置积分时也可设置该参数)" \
                         "\n\t活动积分预算: [300] (可选参数,非负整数类型)" \
                         "\n\t单次参与/打卡积分奖励: [1] (可选参数, 非负整数类型, 若活动设置其他积分配置,则必需配置该项)" \
                         "\n\t最大积分打卡次数: [10] (可选参数)" \
                         "\n\t活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等] (可选参数,可为任意内容, " \
                         "作为活动说明的补充以补充其他活动相关信息)" \
                         "\n]"
        return output_message

    @staticmethod
    def get_new_activity_example() -> str:
        example_message = ".发起活动" \
                          "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                          "\n活动开始时间: [2023-08-01]" \
                          "\n活动结束时间: [2023-08-30]" \
                          "\n活动地点: [线上]" \
                          "\n活动人数限制: [30]" \
                          "\n活动积分预算: [300]" \
                          "\n单次参与/打卡积分奖励: [1]" \
                          "\n最大积分打卡次数: [10]" \
                          "\n活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等]"
        return example_message

    @staticmethod
    def get_update_activity_details() -> str:

        output_message = "\n<.更新活动>\n" \
                         "\n命令类型: [活动命令]" \
                         "\n命令权限: [仅俱乐部管理员可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于管理员修改已发起的俱乐部活动, 以已发起的俱乐部<活动名称>为检索标识进行活动修改," \
                         "可修改除了<活动名称>外的所有可选设定,包括" \
                         "<活动开始时间><活动结束时间><活动地点><活动描述><活动人数限制><活动积分预算><单次参与/打卡积分奖励><最大积分打卡次数>等参数]" \
                         "\n\n参数介绍: [" \
                         "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,待修改的活动名称)" \
                         "\n\t活动开始时间: [2023-08-01] (可选参数, 日期格式按照范例即可,从当日0点1分1秒开始生效)" \
                         "\n\t活动结束时间: [2023-08-30] (可选参数, 日期格式按照范例即可,截止当日23点59分59秒失效)" \
                         "\n\t活动地点: [线上] (可选参数,可替换为任意内容) " \
                         "\n\t活动人数限制: [30] (可选参数,非负整数类型,若活动设置积分,则必需配置该项," \
                         "不设置积分时也可设置该参数)" \
                         "\n\t活动积分预算: [300] (可选参数,非负整数类型,若活动设置其他积分配置,则必需配置该项)" \
                         "\n\t单次参与/打卡积分奖励: [1] (可选参数, 非负整数类型, 若活动设置其他积分配置,则必需配置该项)" \
                         "\n\t最大积分打卡次数: [10] (可选参数,若活动设置其他积分配置,则必需配置该项)" \
                         "\n\t活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等] (可选参数,可为任意内容, " \
                         "作为活动说明的补充以补充其他活动相关信息)" \
                         "\n]"

        return output_message

    @staticmethod
    def get_update_activity_example() -> str:
        example_message = ".更新活动" \
                          "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                          "\n活动开始时间: [2023-08-01]" \
                          "\n活动结束时间: [2023-08-30]" \
                          "\n活动地点: [线上]" \
                          "\n活动人数限制: [30]" \
                          "\n活动积分预算: [300]" \
                          "\n单次参与/打卡积分奖励: [1]" \
                          "\n最大积分打卡次数: [10]" \
                          "\n活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等]"
        return example_message

    @staticmethod
    def get_check_activity_status_details() -> str:
        output_message = "\n<.活动状态>\n" \
                         "\n命令类型: [活动命令]" \
                         "\n命令权限: [仅俱乐部管理员可用]" \
                         "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                         "\n命令介绍: [用于管理员查询已开始活动的参与情况,以此做活动记录." \
                         "\n\tPS:群内使用该命令仅显示参与者信息，私聊使用才会显示打卡内容]" \
                         "\n\n参数介绍: [" \
                         "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,待查询的活动名称)" \
                         "\n]"
        return output_message

    @staticmethod
    def get_check_activity_status_example() -> str:
        example_message = ".活动状态" \
                          "\n活动名称: [XXX俱乐部_X月XX活动A]"
        return example_message

    @staticmethod
    def get_new_participants_details() -> str:
        output_message = "\n<.打卡>\n" \
                         "\n命令类型: [活动命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员参与活动,进行打卡记录." \
                         "\nPS:" \
                         "\n\t1. 处于联动活动的可能性考虑, 参与活动的俱乐部群可以不在其对应的俱乐部," \
                         "也可以在其他激活本工具的群内进行打卡,除俱乐部联动活动外，不建议以此种方式进行打卡." \
                         "\n\t2. 若活动进行了积分配置,会自动进行积分记录." \
                         "\n\t3. 若以达到活动积分上限,或积分预算上限,将不会再进行积分,但是会对打卡内容做保留,计入打卡统计" \
                         "\n\t4. ‼ 为了避免打卡重名的情况,<参与人>选项需要为自己邮箱前缀,即@前的部分 如abc012.zzz@defg.com, " \
                         "则参与人为abc012.zzz ‼" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,待参与的活动名称)" \
                         "\n\t参与人: [aaa.bbb] (必需参数,\n\n‼成员的唯一标识,参与人的邮箱前缀,即@前的部分 如abc012.zzz@defg.com‼)" \
                         "\n\t备注: [打卡内容] (必需参数,可为任意内容，打卡内容)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_new_participants_example() -> str:
        example_message = ".打卡" \
                          "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                          "\n参与人: [aaa.bbb]" \
                          "\n备注: [打卡的内容]"
        return example_message

    @staticmethod
    def get_operate_points_details() -> str:
        output_message = "\n<.操作积分>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [仅俱乐部管理员可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于管理员操作或批量操作俱乐部积分情况,操作选项有1.增加 2.扣除 3.设置为 三种类型." \
                         "可一次性指定多名用户" \
                         "\n\tPS: 操作时，请确认用户名正确,若用户不存在则会直接新建用户账户进行操作" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待操作积分账户所在的俱乐部群名)" \
                         "\n\t姓名: [aaa.bbb ccc.bbb ddd.bbb] (必需参数,待查询的用户,即邮箱前缀,@前的部分 " \
                         "可以为多人 以空格隔开)" \
                         "\n\t积分: [+/-/=10] (必需参数,待操作的积分数额和操作类型," \
                         "+表示增加后接的积分数额,-表示扣除后接的积分数额,=表示强制设置为后接的积分数额)" \
                         "\n\t备注: [积分变化的原因] (可选参数,备注内容，可以填写积分变化的原因)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_operate_points_example() -> str:
        example_message = ".操作积分" \
                          "\n俱乐部群名: [XXX俱乐部]" \
                          "\n姓名: [aaa.bbb ccc.bbb aaa.ddd]" \
                          "\n备注: [修订记录错误积分]" \
                          "\n积分: [+10]" \
                          "\n或者" \
                          "\n积分: [-20]" \
                          "\n或者" \
                          "\n积分: [=30]"
        return example_message

    @staticmethod
    def get_consume_points_details() -> str:
        output_message = "\n<.消费积分>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员消费已获得的俱乐部积分" \
                         "\nPS: " \
                         "\n\t1.消费时仅判断账户名,但是会记录消费人的微信名称和微信号,请勿随意消费他人积分" \
                         f"\n\t2.公共积分账户名为{const_var.COMMON_ACCOUNT_REAL_NAME},可供任意消费" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待操作积分账户所在的俱乐部群名)" \
                         "\n\t姓名: [aaa.bbb] (必需参数,待消费积分的用户,即邮箱前缀,@前的部分) " \
                         "\n\t积分: [10] (必需参数,非负整数类型, 待消费的积分数额)" \
                         "\n\t备注: [消费内容] (可选参数,备注内容，可以填写具体消费内容)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_consume_points_example() -> str:
        example_message = ".消费积分" \
                          "\n俱乐部群名: [XXX俱乐部]" \
                          "\n姓名: [aaa.bbb]" \
                          "\n备注: [兑换奖品:AAA]" \
                          "\n积分: [10]"
        return example_message

    @staticmethod
    def get_donate_points_details() -> str:
        output_message = "\n<.捐献积分>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [仅俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员捐献已获得的俱乐部积分到公共账户" \
                         "\nPS: " \
                         "\n\t1.捐献时仅判断账户名,但是会记录操作人的微信名称和微信号,请勿随意捐献他人积分" \
                         f"\n\t2.积分会捐献到公共积分账户名: {const_var.COMMON_ACCOUNT_REAL_NAME},以供其他成员任意消费" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待操作积分账户所在的俱乐部群名)" \
                         "\n\t姓名: [aaa.bbb] (必需参数,待捐献积分的用户,即邮箱前缀,@前的部分) " \
                         "\n\t积分: [10] (必需参数, 非负整数类型, 待捐献的积分数额)" \
                         "\n\t备注: [捐献积分] (可选参数,备注内容)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_donate_points_example() -> str:
        example_message = ".捐献积分" \
                          "\n俱乐部群名: [XXX俱乐部]" \
                          "\n姓名: [aaa.bbb]" \
                          "\n备注: [捐献积分]" \
                          "\n积分: [10]"
        return example_message

    @staticmethod
    def get_query_points_balance_details() -> str:
        output_message = "\n<.查询积分余额>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员查询指定账户的积分余额" \
                         "\nPS: " \
                         "\n\t1.查询时仅判断账户名,可查询任意用户余额" \
                         f"\n\t2.公共积分账户名: {const_var.COMMON_ACCOUNT_REAL_NAME}" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待操作积分账户所在的俱乐部群名)" \
                         "\n\t姓名: [aaa.bbb] (必需参数,待消费积分的用户,即邮箱前缀,@前的部分) " \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_query_points_balance_example() -> str:
        example_message = ".查询积分余额" \
                          "\n俱乐部群名: [XXX俱乐部]" \
                          "\n姓名: [aaa.bbb]"
        return example_message

    @staticmethod
    def get_query_points_flow_details() -> str:
        output_message = "\n<.查询积分流水>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员查询指定账户的积分流水" \
                         "\nPS: " \
                         "\n\t1.查询时仅判断账户名,可查询任意用户积分流水" \
                         f"\n\t2.公共积分账户名: {const_var.COMMON_ACCOUNT_REAL_NAME}" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待查询积分账户所在的俱乐部群名)" \
                         "\n\t姓名: [aaa.bbb] (必需参数,待查询积分的用户,即邮箱前缀,@前的部分) " \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_query_points_flow_example() -> str:
        example_message = ".查询积分流水" \
                          "\n俱乐部群名: [XXX俱乐部]" \
                          "\n姓名: [aaa.bbb]"
        return example_message

    @staticmethod
    def get_query_points_all_details() -> str:
        output_message = "\n<.查询积分总榜>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员查询俱乐部下所有账户的累计积分排名" \
                         "\nPS: " \
                         "\n1.积分总榜为历史总获得过的积分数额，不是积分余额" \
                         f"\n2.公共积分账户: {const_var.COMMON_ACCOUNT_REAL_NAME} 不计入积分总榜" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待查询俱乐部群名)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_query_points_all_example() -> str:
        example_message = ".查询积分总榜" \
                          "\n俱乐部群名: [XXX俱乐部]"
        return example_message

    @staticmethod
    def get_query_balance_all_details() -> str:
        output_message = "\n<.查询余额总榜>\n" \
                         "\n命令类型: [积分命令]" \
                         "\n命令权限: [所有人可用]" \
                         "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                         "\n命令介绍: [用于俱乐部成员查询俱乐部下所有账户的累计积分排名" \
                         "\nPS: " \
                         "\n1.积分余额总榜,查询到的是目前的积分余额排名,有别于积分总榜" \
                         f"\n2.公共积分账户: {const_var.COMMON_ACCOUNT_REAL_NAME} 计入余额总榜" \
                         "\n]" \
                         "\n\n参数介绍: [" \
                         "\n\t俱乐部群名: [XXX俱乐部] (必需参数,待查询俱乐部群名)" \
                         "\n\n]"
        return output_message

    @staticmethod
    def get_query_balance_all_example() -> str:
        example_message = ".查询余额总榜" \
                          "\n俱乐部群名: [XXX俱乐部]"
        return example_message

    @staticmethod
    def get_help_message(command=const_var.DEFAULT_ACTIVITY_PARAS):
        try:
            output = OutputMessageIterator()
            if command == const_var.DEFAULT_ACTIVITY_PARAS:
                output_message = CommandHelper.get_help_overview_details()
                output_message += "\n" \
                                  "可按照如下格式进行各个命令的详细使用帮助查询"
                output.add_new_message(output_message)

                example_message = CommandHelper.get_help_command_example()
                output.add_new_message(example_message)
                return output
            if command == ".发起活动":
                output_message = CommandHelper.get_new_activity_details()
                output_message += '\n\n' \
                                  '\n完整使用示例如下'
                output.add_new_message(output_message)
                example_message = CommandHelper.get_new_activity_example()
                output.add_new_message(example_message)
                return output
            if command == ".更新活动":
                output_message = CommandHelper.get_update_activity_details()
                output_message += "\n\n" \
                                  "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_update_activity_example()
                output.add_new_message(example_message)
                return output
            if command == ".活动状态":
                output_message = CommandHelper.get_check_activity_status_details()
                output_message += "\n\n" \
                                  "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_check_activity_status_example()
                output.add_new_message(example_message)
                return output
            if command == ".打卡":
                output_message = CommandHelper.get_new_participants_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_new_participants_example()
                output.add_new_message(example_message)
                return output
            if command == ".操作积分":
                output_message = CommandHelper.get_operate_points_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_operate_points_example()
                output.add_new_message(example_message)
                return output
            if command == ".消费积分":
                output_message = CommandHelper.get_consume_points_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_consume_points_example()
                output.add_new_message(example_message)
                return output
            if command == ".捐献积分":
                output_message = CommandHelper.get_donate_points_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_donate_points_example()
                output.add_new_message(example_message)
                return output
            if command == ".查询积分余额":
                output_message = CommandHelper.get_query_points_balance_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_query_points_balance_example()
                output.add_new_message(example_message)
                return output
            if command == ".查询积分流水":
                output_message = CommandHelper.get_query_points_flow_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_query_points_flow_example()
                output.add_new_message(example_message)
                return output
            if command == ".查询积分总榜":
                output_message = CommandHelper.get_query_points_all_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_query_points_all_example()
                output.add_new_message(example_message)
                return output
            if command == ".查询余额总榜":
                output_message = CommandHelper.get_query_balance_all_details()
                output_message += "\n完整使用示例如下"
                output.add_new_message(output_message)
                example_message = CommandHelper.get_query_balance_all_example()
                output.add_new_message(example_message)
                return output
            error_message = "待查询的命令错误."
            raise Exception(error_message)

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"获取帮助信息时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_help_command_example()
            output.add_new_message(example_message)
            return output


class BonusManager:
    @staticmethod
    def get_bonus_account(club_name, club_member_real_name):
        """
        # return bonus account query result, if no bonus account, will create one.
        :param club_name:
        :param club_member_real_name:
        :return:
        """
        existed_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
            filter(db.BonusPoint.club_member_real_name == club_member_real_name).all()
        if len(existed_bonus) <= 0:
            new_bonus = db.BonusPoint(
                club_room_name=club_name,
                club_member_real_name=club_member_real_name,
                related_change_flow_ids="",
                bonus_points_balance=0,
                total_points=0,
            )
            db.table.session.add(new_bonus)
            db.table.session.commit()
        bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
            filter(db.BonusPoint.club_member_real_name == club_member_real_name).first()
        return bonus

    @staticmethod
    def new_bonus_flow(club_room_id, club_room_name, club_member_real_name,
                       operator_id, operator_name, previous_point, point_after_operation,
                       activity_flow_id=None, bonus_flow_type=const_var.BONUS_FLOW_TYPE_INCREASE,
                       operator_real_name=const_var.AUTO_BONUS_OPERATOR_REAL_NAME,
                       comments="",
                       ):
        """
        Bonus account will also be updated here
        :param club_room_id:
        :param club_room_name: 
        :param club_member_real_name: 
        :param operator_id: 
        :param operator_name: 
        :param previous_point: 
        :param point_after_operation: 
        :param activity_flow_id: 
        :param bonus_flow_type: 
        :param operator_real_name:
        :param comments
        :return: 
        """
        bonus_account = BonusManager.get_bonus_account(club_room_name, club_member_real_name)
        # make a new bonus flow
        new_bonus_flow = db.BonusPointFlow(
            bonus_point_id=bonus_account.bonus_point_id,
            club_room_id=club_room_id,
            club_room_name=club_room_name,
            bonus_flow_type=bonus_flow_type,
            operator_id=operator_id,
            operator_name=operator_name,
            operator_real_name=operator_real_name,
            club_member_real_name=club_member_real_name,
            activity_flow_id=activity_flow_id,
            previous_point=previous_point,
            point_after_operation=point_after_operation,
            operation_date=datetime.now(),
            bonus_flow_comments=comments,
        )
        db.table.session.add(new_bonus_flow)
        db.table.session.commit()

        # update bonus account with new bonus flow
        bonus_flow = db.table.session.query(db.BonusPointFlow) \
            .filter(db.BonusPointFlow.club_room_name == club_room_name) \
            .filter(db.BonusPointFlow.club_member_real_name == club_member_real_name) \
            .order_by(db.BonusPointFlow.bonus_flow_id.desc()).first()
        bonus_account.last_changed_flow_id = bonus_flow.bonus_flow_id
        bonus_account.related_change_flow_ids += f" {bonus_flow.bonus_flow_id}"
        bonus_account.bonus_points_balance = point_after_operation
        if point_after_operation - previous_point > 0:
            bonus_account.total_points += point_after_operation - previous_point

        db.table.session.commit()

    @staticmethod
    def operate_bonus_points(club_name: str,
                             operator_id: str, operator_name: str,
                             target_real_names: list,
                             operator_real_name=const_var.ADMIN_BONUS_OPERATOR_REAL_NAME,
                             increased_points=const_var.DEFAULT_ACTIVITY_PARAS,
                             decreased_points=const_var.DEFAULT_ACTIVITY_PARAS,
                             set_to_points=const_var.DEFAULT_ACTIVITY_PARAS,
                             comments="",
                             ):
        try:
            output = OutputMessageIterator()
            output_message = f""
            if len(target_real_names) <= 0:
                error_message = f"待操作积分账户姓名无效"
                raise Exception(error_message)
            # check club name
            club_room_id = None  # TODO
            if increased_points is not const_var.DEFAULT_ACTIVITY_PARAS:
                increased_points = int(increased_points.replace("+", ""))
                for real_name in target_real_names:
                    output_message = f""
                    previous_point = BonusManager.get_bonus_account(club_name=club_name,
                                                                    club_member_real_name=real_name) \
                        .bonus_points_balance
                    point_after_operation = previous_point + increased_points
                    BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                                club_room_name=club_name,
                                                club_member_real_name=real_name,
                                                operator_id=operator_id,
                                                operator_name=operator_name,
                                                previous_point=previous_point,
                                                point_after_operation=point_after_operation,
                                                bonus_flow_type=const_var.BONUS_FLOW_TYPE_INCREASE,
                                                operator_real_name=operator_real_name,
                                                comments=comments,
                                                )
                    output_message += f"\n在俱乐部群[{club_name}]积分记录中, 用户[{real_name}]" \
                                      f"积分增长[{increased_points}]点, " \
                                      f"目前余额[{point_after_operation}] "
                    output.add_new_message(output_message)
                return output

            if decreased_points is not const_var.DEFAULT_ACTIVITY_PARAS:
                decreased_points = int(decreased_points.replace("-", ""))
                for real_name in target_real_names:
                    output_message = f""
                    previous_point = BonusManager.get_bonus_account(club_name=club_name,
                                                                    club_member_real_name=real_name) \
                        .bonus_points_balance
                    point_after_operation = previous_point - decreased_points
                    if point_after_operation < 0:
                        output_message += f"\n在俱乐部群[{club_name}]积分记录中,用户[{real_name}]积分余额为[{previous_point}]" \
                                          f"\n无法扣除积分[{decreased_points}]点"
                        output.add_new_message(output_message)
                        continue
                    BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                                club_room_name=club_name,
                                                club_member_real_name=real_name,
                                                operator_id=operator_id,
                                                operator_name=operator_name,
                                                previous_point=previous_point,
                                                point_after_operation=point_after_operation,
                                                bonus_flow_type=const_var.BONUS_FLOW_TYPE_DECREASE,
                                                operator_real_name=operator_real_name,
                                                comments=comments,
                                                )
                    output_message += f"\n在俱乐部群[{club_name}]积分记录中, 用户[{real_name}]" \
                                      f"积分扣除[{decreased_points}]点, " \
                                      f"目前余额[{point_after_operation}] "
                    output.add_new_message(output_message)
                return output

            if set_to_points is not const_var.DEFAULT_ACTIVITY_PARAS:
                set_to_points = int(set_to_points.replace("=", ""))
                for real_name in target_real_names:
                    previous_point = BonusManager.get_bonus_account(club_name=club_name,
                                                                    club_member_real_name=real_name) \
                        .bonus_points_balance
                    point_after_operation = set_to_points
                    BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                                club_room_name=club_name,
                                                club_member_real_name=real_name,
                                                operator_id=operator_id,
                                                operator_name=operator_name,
                                                previous_point=previous_point,
                                                point_after_operation=point_after_operation,
                                                bonus_flow_type=const_var.BONUS_FLOW_TYPE_SET_TO,
                                                operator_real_name=operator_real_name,
                                                comments=comments,
                                                )
                    output_message += f"\n在俱乐部群[{club_name}]积分记录中, 用户[{real_name}]" \
                                      f"积分设定为[{set_to_points}]点 "
                    output.add_new_message(output_message)
                return output
            error_message = f"未知操作命令"
            raise Exception(error_message)

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"操作积分时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_operate_points_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def consume_bonus_points(club_name: str,
                             operator_id: str, operator_name: str,
                             target_real_name: str,
                             consumed_points: int,
                             operator_real_name: str,
                             comments="",
                             ):
        try:
            output = OutputMessageIterator()
            output_message = f""
            club_room_id = ""
            previous_point = BonusManager.get_bonus_account(club_name=club_name, club_member_real_name=target_real_name) \
                .bonus_points_balance
            point_after_operation = previous_point - consumed_points
            if point_after_operation < 0:
                error_message = f"\n在俱乐部群[{club_name}]积分记录中,用户[{target_real_name}]余额为{previous_point}" \
                                f"\n无法消费[{consumed_points}]点积分"
                raise Exception(error_message)
            BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                        club_room_name=club_name,
                                        club_member_real_name=target_real_name,
                                        operator_id=operator_id,
                                        operator_name=operator_name,
                                        previous_point=previous_point,
                                        point_after_operation=point_after_operation,
                                        bonus_flow_type=const_var.BONUS_FLOW_TYPE_DECREASE,
                                        operator_real_name=operator_real_name,
                                        comments=comments,
                                        )
            output_message += f"\n在俱乐部群[{club_name}]积分记录中, 用户[{target_real_name}]成功消费[{consumed_points}]点积分" \
                              f"\n目前积分余额为: [{point_after_operation}]"
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"消费积分时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_operate_points_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def donate_bonus_points(club_name: str, club_member_real_name: str,
                            operator_id: str, operator_name: str, donated_points: int,
                            comments="",
                            ):
        try:
            output = OutputMessageIterator()
            output_message = f""
            club_room_id = ""
            common_account = BonusManager.get_bonus_account(club_name=club_name,
                                                            club_member_real_name=const_var.COMMON_ACCOUNT_REAL_NAME)
            source_account = BonusManager.get_bonus_account(club_name=club_name,
                                                            club_member_real_name=club_member_real_name)

            # source consume
            previous_point = source_account.bonus_points_balance
            point_after_operation = source_account.bonus_points_balance - donated_points
            if point_after_operation < 0:
                error_message = f"\n在俱乐部群[{club_name}]积分记录中,用户[{club_member_real_name}]余额为{previous_point}" \
                                  f"\n无法捐献[{donated_points}]点积分"
                raise Exception(error_message)
            BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                        club_room_name=club_name,
                                        club_member_real_name=club_member_real_name,
                                        operator_id=operator_id,
                                        operator_name=operator_name,
                                        previous_point=source_account.bonus_points_balance,
                                        point_after_operation=source_account.bonus_points_balance - donated_points,
                                        bonus_flow_type=const_var.BONUS_FLOW_TYPE_DECREASE,
                                        operator_real_name=club_member_real_name,
                                        comments=comments,
                                        )
            common_points_after_operation = source_account.bonus_points_balance + donated_points
            BonusManager.new_bonus_flow(club_room_id=club_room_id,
                                        club_room_name=club_name,
                                        club_member_real_name=const_var.COMMON_ACCOUNT_REAL_NAME,
                                        operator_id=operator_id,
                                        operator_name=operator_name,
                                        previous_point=source_account.bonus_points_balance,
                                        point_after_operation=common_points_after_operation,
                                        bonus_flow_type=const_var.BONUS_FLOW_TYPE_INCREASE,
                                        operator_real_name=club_member_real_name,
                                        comments=comments,
                                        )
            output_message += f"在俱乐部群[{club_name}]积分记录中,用户[{club_member_real_name}]成功捐献[{donated_points}]点积分" \
                              f"\n目前用户账户余额:[{point_after_operation}]" \
                              f"\n公共账户[{const_var.COMMON_ACCOUNT_REAL_NAME}]余额为[{common_points_after_operation}]"
            output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"捐献积分时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_donate_points_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def query_bonus_points_balance(club_name: str, club_member_real_name: str):
        try:
            output_message = ""
            output = OutputMessageIterator()
            balance = BonusManager.get_bonus_account(club_name=club_name, club_member_real_name=club_member_real_name) \
                .bonus_points_balance
            output_message += f"在俱乐部群[{club_name}]积分记录中,用户[{club_member_real_name}]积分余额为[{balance}]"
            output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分余额时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_balance_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def query_bonus_points_flow(club_name: str, club_member_real_name: str):
        try:
            output_counts_per_message = 5
            output = OutputMessageIterator()
            output_message = ""
            existed_flows = db.table.session.query(db.BonusPointFlow) \
                .filter(db.BonusPointFlow.club_room_name == club_name) \
                .filter(db.BonusPointFlow.club_member_real_name == club_member_real_name) \
                .order_by(db.BonusPointFlow.bonus_flow_id.desc()) \
                .all()
            if len(existed_flows) <= 0:
                error_message = f"\n在俱乐部群[{club_member_real_name}]积分记录中用户[{club_name}]无积分流水记录"
                raise Exception(error_message)
            output_message += f"<积分流水>" \
                              f"\n用户名: [{club_member_real_name}]" \
                              f"\n俱乐部群名:[{club_name}]"
            output.add_new_message(output_message)
            count = 0
            output_message = ""
            for flow in existed_flows:
                count += 1
                if count % output_counts_per_message == 0:
                    output_message = f"\n流水ID#{flow.bonus_flow_id}" \
                                     f"\n操作前积分:{flow.previous_point}" \
                                     f"\n操作后积分: {flow.point_after_operation}" \
                                     f"\n操作人微信ID: {flow.operator_id}" \
                                     f"\n操作人微信昵称: {flow.operator_name}" \
                                     f"\n操作用户: {flow.operator_real_name}" \
                                     f"\n操作执行日期: {flow.operation_date}" \
                                     f"\n操作备注: {flow.bonus_flow_comments}\n"
                    output.add_new_message(output_message)
                else:
                    output_message += f"\n流水ID#{flow.bonus_flow_id}" \
                                      f"\n操作前积分:{flow.previous_point}" \
                                      f"\n操作后积分: {flow.point_after_operation}" \
                                      f"\n操作人微信ID: {flow.operator_id}" \
                                      f"\n操作人微信昵称: {flow.operator_name}" \
                                      f"\n操作用户: {flow.operator_real_name}" \
                                      f"\n操作执行日期: {flow.operation_date}" \
                                      f"\n操作备注: {flow.bonus_flow_comments}\n"
            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)

            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分流水时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_flow_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def query_bonus_points_all(club_name: str):
        try:
            output_counts_per_message = 5
            output = OutputMessageIterator()
            output_message = ""
            all_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
                order_by(db.BonusPoint.bonus_points_balance.desc()).all()
            if len(all_bonus) <= 0:
                error_message = f"俱乐部群[{club_name}]积分系统中尚无用户"
                raise Exception(error_message)

            count = 0
            output_message += f"\n俱乐部群[{club_name}]累计获得积分排名如下:\n"
            output.add_new_message(output_message)
            output_message = ""
            for bonus in all_bonus:
                if bonus.club_member_real_name == const_var.COMMON_ACCOUNT_REAL_NAME:
                    continue
                count += 1
                if count % output_counts_per_message == 0:
                    output_message = f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                     f"累计获得积分: [{bonus.total_points}]"
                    output.add_new_message(output_message)
                else:
                    output_message += f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                      f"累计获得积分: [{bonus.total_points}]"

            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分总榜时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_all_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def query_balance_all(club_name: str):
        try:
            output_counts_per_message = 5
            output = OutputMessageIterator()
            output_message = ""
            all_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
                order_by(db.BonusPoint.bonus_points_balance.desc()).all()
            if len(all_bonus) <= 0:
                error_message = f"俱乐部群[{club_name}]积分系统中尚无用户"
                raise Exception(error_message)

            count = 0
            output_message += f"\n俱乐部群[{club_name}]积分余额排名如下:\n"
            output.add_new_message(output_message)
            output_message = ""
            for bonus in all_bonus:
                count += 1
                if count % output_counts_per_message == 0:
                    output_message = f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                     f"积分余额: [{bonus.bonus_points_balance}]"
                    output.add_new_message(output_message)
                else:
                    output_message += f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                      f"积分余额: [{bonus.bonus_points_balance}]"
            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分余额榜时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_balance_all_example()
            output.add_new_message(example_message)
            return output


class ClubActivityManager:
    @staticmethod
    def get_activity(title):
        """
        :param title: activity title
        :return: the existed activity db
        """

        existed_activities = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title) \
            .all()
        if len(existed_activities) <= 0:
            error_message = f"活动名称[{title}]不存在"
            raise Exception(error_message)
        return existed_activities[0]

    @staticmethod
    def new_activity(room_id, room_name, title, full_content, description,
                     organizer_id, organizer_name,
                     place, planed_people,
                     point_budget, point, max_earn_count,
                     start_date, end_date):
        """
        PS: All default value handled by previous layer
        :param room_id: room id
        :param room_name: the name of room
        :param title: activity title
        :param full_content: full activity content
        :param description:
        :param organizer_id: the wxid of organizer
        :param organizer_name: the nickname of organizer
        :param place: activity place
        :param point_budget: total points budget
        :param point: point per joining can earn
        :param max_earn_count: max earn count for a single person
        :param planed_people: planed people of an activity
        :param start_date: type is datetime, the first day of activity
        :param end_date: type is datetime, the last day of activity
        :return:
        """
        try:
            # if activity already existed
            output = OutputMessageIterator()
            query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)
            if len(query.all()) > 0:
                error_message = f"活动名称[{title}]已存在，请重新设置新的活动名称后重试"
                raise Exception(error_message)
            # bonus setting should be synced
            # if point + max_earn_count + point_budget != 3 * const_var.DEFAULT_ACTIVITY_PARAS \
            #         and point + max_earn_count + point_budget < 0:
            #     # != 3* defaults means, not all default
            #     # < 0 means any of them set  to default
            #     error_message = f"{title} activity points set error, please check again."
            #     raise Exception(error_message)
            # if didn't exist
            activity = db.ClubActivity(
                club_room_id=room_id,
                club_room_name=room_name,
                activity_title=title,
                activity_description=description,
                activity_full_content=full_content,
                activity_organizer_id=organizer_id,
                activity_organizer_name=organizer_name,
                activity_create_date=datetime.now(),
                activity_planed_people=planed_people,
                activity_place=place,
                activity_point_budget=point_budget,
                activity_point=point,
                activity_max_count=max_earn_count,
                activity_start_date=start_date,
                activity_end_date=end_date,
                activity_candidates=0,
                activity_candidates_name="",
                activity_consumed_budget=0,
            )
            db.table.session.add(activity)
            db.table.session.commit()
            output_message = f"发起活动[{title}]成功"
            output.add_new_message(output_message)
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"发起活动时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_new_activity_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def update_activity(title,
                        description=const_var.DEFAULT_ACTIVITY_PARAS,
                        place=const_var.DEFAULT_ACTIVITY_PARAS,
                        planed_people=const_var.DEFAULT_ACTIVITY_PARAS,
                        point_budget=const_var.DEFAULT_ACTIVITY_PARAS,
                        point=const_var.DEFAULT_ACTIVITY_PARAS,
                        max_earn_count=const_var.DEFAULT_ACTIVITY_PARAS,
                        start_date=const_var.DEFAULT_ACTIVITY_PARAS,
                        end_date=const_var.DEFAULT_ACTIVITY_PARAS,
                        ):
        """
        PS: only title and target optional must be here
        :param title: activity title
        :param description:
        :param place: activity place
        :param point_budget: total points budget
        :param point: point per joining can earn
        :param max_earn_count: max earn count for a single person
        :param planed_people: planed people of an activity
        :param start_date: type is datetime, the first day of activity
        :param end_date: type is datetime, the last day of activity
        :return:
        """
        try:
            ## check title correct
            output = OutputMessageIterator()
            output_message = ""
            activity = ClubActivityManager.get_activity(title)

            if description is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"活动描述更新为: [{description}]"
                activity.activity_description = description
            if planed_people is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n活动人数限制从" \
                                  f"[{activity.activity_planed_people}]更新为[{planed_people}]"
                activity.activity_planed_people = planed_people
            if place is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n活动地点从" \
                                  f"{activity.activity_place}更新为[{place}]"
                activity.activity_place = place
            if point_budget is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n活动积分预算从" \
                                  f"[{activity.activity_point_budget}]更新为[{point_budget}]"
                activity.activity_point_budget = point_budget
            if point is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n单次参与/打卡积分奖励从" \
                                  f"[{activity.activity_point}]更新为[{point}]"
                activity.activity_point = point
            if max_earn_count is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n最大积分打卡次数从" \
                                  f"[{activity.activity_max_count}]更新为[{max_earn_count}]"
                activity.activity_max_count = max_earn_count
            if start_date is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n活动开始时间从[{activity.activity_start_date}]" \
                                  f"更新为[{start_date}]"
                activity.activity_start_date = start_date
            if end_date is not const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n活动结束时间从[{activity.activity_end_date}]" \
                                  f"更新为[{end_date}]"
                activity.activity_end_date = end_date
            activity.activity_full_content += output_message
            # # if activity already existed,update it
            # query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)

            db.table.session.commit()
            output_message += f"\n活动[{title}]已更新"
            output.add_new_message(output_message)
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"更新活动时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_update_activity_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def new_participates(title, partici_id, partici_name, partici_real_name, content, comments=""):
        """
        :param title: activity title, as activity name is associated with club name, so no need for it
        :param partici_id: the participated wxid
        :param partici_name: the participated  nickname
        :param content: the activity participation content
        :param partici_real_name: real name
        :return:
        """
        try:
            output = OutputMessageIterator()
            output_message = ""
            # check activity status
            activity = ClubActivityManager.get_activity(title)

            activity_id = activity.activity_id
            # get end datetime from title
            activity_end_date = activity.activity_end_date
            if datetime.now() > activity_end_date:
                error_message = f"活动[{title}]已于[{activity_end_date}]结束"
                raise Exception(error_message)

            candidates_name = activity.activity_candidates_name.split(" ")
            if partici_real_name not in candidates_name:
                activity.activity_candidates += 1
                activity.activity_candidates_name += f" {partici_real_name}"
            # planed people handle
            left_seats = activity.activity_planed_people - activity.activity_candidates
            if activity.activity_planed_people != const_var.DEFAULT_ACTIVITY_PARAS:
                if left_seats < 0 and partici_real_name not in candidates_name:
                    error_message = f"活动人数已满" \
                                    f"\n人数限制:{activity.activity_planed_people} " \
                                    f"\n已参与人数: {activity.activity_candidates} "
                    raise Exception(error_message)
                output_message += f"\n剩余可参与人数: [{left_seats}]"
            output_message += f" \n 用户[{partici_real_name}]参与活动[{title}]成功\n"

            # activity flow

            all_previous_earned = 0
            ## get last activity flow
            all_joined_flows = db.table.session.query(db.ClubActivityFlow) \
                .filter(db.ClubActivityFlow.activity_id == activity.activity_id) \
                .filter(db.ClubActivityFlow.activity_participates_real_name == partici_real_name) \
                .order_by(db.ClubActivityFlow.activity_flow_id.desc()) \
                .all()
            if len(all_joined_flows) > 0:
                last_joined_flow = all_joined_flows[0]
                all_previous_earned = last_joined_flow.activity_point_earned

            participates = db.ClubActivityFlow(
                activity_flow_content=content,
                activity_id=activity_id,
                activity_participates_id=partici_id,
                activity_participates_name=partici_name,
                activity_participates_real_name=partici_real_name,
                activity_point_earned=all_previous_earned,
                activity_flow_creat_date=datetime.now(),
                join_comments=comments,
            )
            db.table.session.add(participates)
            db.table.session.commit()
            output.add_new_message(output_message)

            # bonus flow

            ## according title to check if we need to update bonus
            ## check if bonus set in this activity
            if activity.activity_point == const_var.DEFAULT_ACTIVITY_PARAS \
                    :
                db.table.session.commit()
                return output

            ## if no more budget
            if activity.activity_point_budget != const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_consumed_budget + activity.activity_point > activity.activity_point_budget:
                db.table.session.commit()
                output_message = f" 该活动积分预算不足,本次打卡不增加积分" \
                                 f" \n活动积分预算: {activity.activity_point_budget} " \
                                 f" \n活动已消耗积分: {activity.activity_consumed_budget} "
                output.add_new_message(output_message)
                return output

            ## if already reached max earned points

            # PS: the last one, is current operating one, for
            current_flow = db.table.session.query(db.ClubActivityFlow) \
                .filter(db.ClubActivityFlow.activity_id == activity.activity_id) \
                .filter(db.ClubActivityFlow.activity_participates_real_name == partici_real_name) \
                .order_by(db.ClubActivityFlow.activity_flow_id.desc()) \
                .first()
            if activity.activity_max_count != const_var.DEFAULT_ACTIVITY_PARAS \
                    and all_previous_earned + activity.activity_point > activity.activity_max_count * activity.activity_point:
                current_flow.activity_point_earned = all_previous_earned
                output_message = f" \n 已达到本次活动最大可获得积分的打卡次数上限, 本次打卡不增加积分" \
                                 f" \n 最大积分次数: {activity.activity_max_count} " \
                                 f" \n 已获得积分的打卡次数: {all_previous_earned / activity.activity_point}"
                db.table.session.commit()
                output.add_new_message(output_message)
                return output
            # can add points
            current_flow.activity_point_earned += activity.activity_point

            # new bonus flow
            previous_point_balance = BonusManager.get_bonus_account(club_name=activity.club_room_name,
                                                                    club_member_real_name=partici_real_name) \
                .total_points
            comments = f"活动[{title}]打卡成功"
            BonusManager.new_bonus_flow(club_room_id=activity.club_room_id,
                                        club_room_name=activity.club_room_name,
                                        club_member_real_name=partici_real_name,
                                        operator_id=activity.activity_organizer_id,
                                        operator_name=activity.activity_organizer_name,
                                        previous_point=previous_point_balance,
                                        point_after_operation=previous_point_balance + activity.activity_point,
                                        activity_flow_id=current_flow.activity_flow_id,
                                        comments=comments,
                                        )
            activity.activity_consumed_budget += activity.activity_point
            bonus_account = BonusManager.get_bonus_account(club_name=activity.club_room_name,
                                                           club_member_real_name=partici_real_name)
            output_message = f"新增积分[{activity.activity_point}]" \
                             f"该活动剩余积分预算: " \
                             f"[{activity.activity_point_budget - activity.activity_consumed_budget}]" \
                             f"在俱乐部群[{activity.club_room_name}]积分账户中" \
                             f"用户[{partici_real_name}]累计获得的总积分为: " \
                             f"[{bonus_account.total_points}] " \
                             f"目前积分余额为: [{bonus_account.bonus_points_balance}]"
            output.add_new_message(output_message)
            db.table.session.commit()
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"打卡时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_new_participants_example()
            output.add_new_message(example_message)
            return output

    @staticmethod
    def show_activity_status(title, show_flag: int = 1):
        """
        :param title:
        :param show_flag, 1-> name, 2-> date, 4-> content, 8(TODO)-> name,date,content,points change
        :return:
        """
        try:
            output = OutputMessageIterator()
            activity = ClubActivityManager.get_activity(title)
            activity_id = activity.activity_id

            existed = db.table.session.query(db.ClubActivityFlow). \
                filter(db.ClubActivityFlow.activity_id == activity_id).all()
            if len(existed) <= 0:
                error_message = f"活动流水 [{title}] 不存在"
                raise Exception(error_message)
            result = f"\n活动名称:{title}"
            output.add_new_message(output)
            count = 0
            for flow in existed:
                count += 1
                result = f"\n#{count}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_NAME:  # name
                    result += f"\n姓名:{flow.activity_participates_real_name}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_DATE:  # date
                    result += f"\n日期:{flow.activity_flow_creat_date}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_CONTENT:  # content
                    result += f"\n打卡内容:\n[{flow.join_comments}]"
                output.add_new_message(result)
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询活动状态时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_check_activity_status_example()
            output.add_new_message(example_message)
            return output
