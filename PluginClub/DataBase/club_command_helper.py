from PluginClub.DataBase.club_utils import OutputMessageIterator
import PluginClub.DataBase.const_var as const_var

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
        output_message = f"\n<.发起活动>\n" \
                         f"\n命令类型: [活动命令]" \
                         f"\n命令权限: [仅俱乐部管理员可用]" \
                         f"\n命令调用: [仅俱乐部群聊可用]" \
                         f"\n命令介绍: [用于管理员发起俱乐部活动, 以发起活动的群名作为俱乐部名称，作为识别俱乐部的唯一标识." \
                         f"可设定作为唯一标识的<活动名称>, 设定<活动开始时间><活动结束时间> " \
                         f"以及可选设置<活动地点><活动描述><活动人数限制><活动积分预算><单次参与/打卡积分奖励><最大积分打卡次数>等参数]" \
                         f"\n\n参数介绍: [" \
                         f"\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,名称可任意,但是需要保证活动名称唯一)" \
                         f"\n\t活动开始时间: [2023-08-01] (必需参数, 日期格式按照范例即可,从当日0点1分1秒开始生效)" \
                         f"\n\t活动结束时间: [2023-08-30] (必需参数, 日期格式按照范例即可,截止当日23点59分59秒失效)" \
                         f"\n\t活动地点: [线上] (可选参数,可为任意内容) " \
                         f"\n\t活动人数限制: [30] (可选参数,非负整数类型" \
                         f"不设置积分时也可设置该参数)" \
                         f"\n\t活动积分预算: [300] (可选参数,非负整数类型)" \
                         f"\n\t单次参与/打卡积分奖励: [1] (可选参数, 非负整数类型, 若活动设置其他积分配置,则必需配置该项)" \
                         f"\n\t单日可积分打卡次数: [1] (可选参数, 非负整数类型)" \
                         f"\n\t最大积分打卡次数: [3] (可选参数, 非负整数类型)" \
                         f"\n\t活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等] (可选参数,可为任意内容, " \
                         f"作为活动说明的补充以补充其他活动相关信息)" \
                         f"\n]"
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
                          "\n单日可积分打卡次数: [1]" \
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
                         "\n\t单次参与/打卡积分奖励: [1] (可选参数, 非负整数类型,)" \
                         "\n\t单日可积分打卡次数: [1] (可选参数,非负整数类型)" \
                         "\n\t最大积分打卡次数: [10] (可选参数,非负整数类型)" \
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
                          "\n单日可积分打卡次数: [1]" \
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
                         "\n\t参与人: [aaa.bbb] (必需参数,\n\n‼成员的唯一标识,参与人的邮箱前缀,即@前的部分 如abc012.zzz@defg.com," \
                         "则参与人为: abc012.zzz‼)" \
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

