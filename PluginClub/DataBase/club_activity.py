from datetime import datetime

import PluginClub.DataBase.club_db as db
import const_var


class CommandHelper:
    @staticmethod
    def get_help_message(command=const_var.DEFAULT_ACTIVITY_PARAS):
        try:
            result_content = ""
            if command == const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += "\n可用命令如下:\n" \
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
                                  ".查询余额总榜    -- 用于查询积分余额的积分榜\n" \
                                  "\n" \
                                  "可按照如下格式进行各个命令的详细使用帮助查询" \
                                  "\n\n.帮助" \
                                  "\n命令名: [命令]"
                return result_content
            if command == ".发起活动":
                result_content += "\n<.发起活动>\n" \
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
                                  "\n\t活动人数限制: [30] (可选参数,非负整数类型,若活动设置积分,则必需配置该项," \
                                  "不设置积分时也可设置该参数)" \
                                  "\n\t活动积分预算: [300] (可选参数,非负整数类型,若活动设置其他积分配置,则必需配置该项)" \
                                  "\n\t单次参与/打卡积分奖励: [1] (可选参数, 非负整数类型, 若活动设置其他积分配置,则必需配置该项)" \
                                  "\n\t最大积分打卡次数: [10] (可选参数,若活动设置其他积分配置,则必需配置该项)" \
                                  "\n\t活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等] (可选参数,可为任意内容, " \
                                  "作为活动说明的补充以补充其他活动相关信息)" \
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.发起活动" \
                                  "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                                  "\n活动开始时间: [2023-08-01]" \
                                  "\n活动结束时间: [2023-08-30]" \
                                  "\n活动地点: [线上]" \
                                  "\n活动人数限制: [30]" \
                                  "\n活动积分预算: [300]" \
                                  "\n单次参与/打卡积分奖励: [1]" \
                                  "\n最大积分打卡次数: [10]" \
                                  "\n活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等]"
                return result_content
            if command == ".更新活动":
                result_content += "\n<.更新活动>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.更新活动" \
                                  "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                                  "\n活动开始时间: [2023-08-01]" \
                                  "\n活动结束时间: [2023-08-30]" \
                                  "\n活动地点: [线上]" \
                                  "\n活动人数限制: [30]" \
                                  "\n活动积分预算: [300]" \
                                  "\n单次参与/打卡积分奖励: [1]" \
                                  "\n最大积分打卡次数: [10]" \
                                  "\n活动描述: [XXX俱乐部XXX活动,有积分,打卡制,打卡内容限制XXXX等]"
                return result_content
            if command == ".活动状态":
                result_content += "\n<.活动状态>\n" \
                                  "\n命令类型: [活动命令]" \
                                  "\n命令权限: [仅俱乐部管理员可用]" \
                                  "\n命令调用: [私聊可用 俱乐部群聊可用]" \
                                  "\n命令介绍: [用于管理员查询已开始活动的参与情况,以此做活动记录." \
                                  "\n\tPS:群内使用该命令仅显示参与者信息，私聊使用才会显示打卡内容]" \
                                  "\n\n参数介绍: [" \
                                  "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,待查询的活动名称)" \
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.活动状态" \
                                  "\n活动名称: [XXX俱乐部_X月XX活动A]"
                return result_content
            if command == ".打卡":
                result_content += "\n<.打卡>\n" \
                                  "\n命令类型: [活动命令]" \
                                  "\n命令权限: [所有人可用]" \
                                  "\n命令调用: [仅俱乐部群聊可用]" \
                                  "\n命令介绍: [用于俱乐部成员参与活动,进行打卡记录." \
                                  "\nPS:" \
                                  "\n\t1. 处于联动活动的可能性考虑, 参与活动的俱乐部群可以不在其对应的俱乐部," \
                                  "也可以在其他激活本工具的群内进行打卡,除俱乐部联动活动外，不建议以此种方式进行打卡." \
                                  "\n\t2. 若活动进行了积分配置,会自动进行积分记录." \
                                  "\n\t3. 若以达到活动积分上限,或积分预算上限,将不会再进行积分,但是会对打卡内容做保留,计入打卡统计" \
                                  "\n\t4. ！！为了避免打卡重名的情况,<参与人>选项需要为自己邮箱前缀,即@前的部分 如abc012.zzz@defg.com, " \
                                  "则参与人为abc012.zzz！！" \
                                  "\n\t5. ！！为了避免打卡重名的情况,<参与人>选项需要为自己邮箱前缀,即@前的部分 如abc012.zzz@defg.com, " \
                                  "则参与人为abc012.zzz！！" \
                                  "\n\t6. ！！为了避免打卡重名的情况,<参与人>选项需要为自己邮箱前缀,即@前的部分 如abc012.zzz@defg.com, " \
                                  "则参与人为abc012.zzz！！" \
                                  "\n]" \
                                  "\n\n参数介绍: [" \
                                  "\n\t活动名称: [XXX俱乐部_X月XX活动A] (必需参数,待参与的活动名称)" \
                                  "\n\t参与人: [aaa.bbb] (必需参数,\n\n成员的唯一标识,参与人的邮箱前缀,即@前的部分 如abc012.zzz@defg.com)" \
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.打卡" \
                                  "\n活动名称: [XXX俱乐部_X月XX活动A]" \
                                  "\n参与人: [aaa.bbb]"
                return result_content
            if command == ".操作积分":
                result_content += "\n<.操作积分>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.操作积分" \
                                  "\n俱乐部群名: [XXX俱乐部]" \
                                  "\n姓名: [aaa.bbb ccc.bbb aaa.ddd]" \
                                  "\n备注: [修订记录错误积分]" \
                                  "\n积分: [+10]" \
                                  "\n或者" \
                                  "\n积分: [-20]" \
                                  "\n或者" \
                                  "\n积分: [=30]"
                return result_content
            if command == ".消费积分":
                result_content += "\n<.消费积分>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.消费积分" \
                                  "\n俱乐部群名: [XXX俱乐部]" \
                                  "\n姓名: [aaa.bbb]" \
                                  "\n备注: [兑换奖品:AAA]" \
                                  "\n积分: [10]"
                return result_content
            if command == ".捐献积分":
                result_content += "\n<.捐献积分>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.捐献积分" \
                                  "\n俱乐部群名: [XXX俱乐部]" \
                                  "\n姓名: [aaa.bbb]" \
                                  "\n备注: [捐献积分]" \
                                  "\n积分: [10]"
                return result_content
            if command == ".查询积分余额":
                result_content += "\n<.查询积分余额>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.查询积分余额" \
                                  "\n俱乐部群名: [XXX俱乐部]" \
                                  "\n姓名: [aaa.bbb]"
                return result_content
            if command == ".查询积分流水":
                result_content += "\n<.查询积分流水>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.查询积分流水" \
                                  "\n俱乐部群名: [XXX俱乐部]" \
                                  "\n姓名: [aaa.bbb]"
                return result_content
            if command == ".查询积分总榜":
                result_content += "\n<.查询积分总榜>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.查询积分总榜" \
                                  "\n俱乐部群名: [XXX俱乐部]"
                return result_content
            if command == ".查询余额总榜":
                result_content += "\n<.查询余额总榜>\n" \
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
                                  "\n\n]" \
                                  "\n完整使用示例如下" \
                                  "\n\n.查询余额总榜" \
                                  "\n俱乐部群名: [XXX俱乐部]"
                return result_content
            result_content += "Invalid target command, please check and retry"
            return result_content

        except Exception as e:
            error_message = f"Error in get help message :{e}"
            raise Exception(error_message)


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
            result_content = f""
            if len(target_real_names) <= 0:
                error_message = f"No valid target names"
                raise Exception(error_message)
            # check club name
            club_room_id = None  # TODO
            if increased_points is not const_var.DEFAULT_ACTIVITY_PARAS:
                increased_points = int(increased_points.replace("+", ""))
                for real_name in target_real_names:
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
                    result_content += f" \n for user [{real_name}] points in club [{club_name}] " \
                                      f"increased by [{increased_points}], " \
                                      f"now is [{point_after_operation}] "
                return result_content

            if decreased_points is not const_var.DEFAULT_ACTIVITY_PARAS:
                decreased_points = int(decreased_points.replace("-", ""))
                for real_name in target_real_names:
                    previous_point = BonusManager.get_bonus_account(club_name=club_name,
                                                                    club_member_real_name=real_name) \
                        .bonus_points_balance
                    point_after_operation = previous_point - decreased_points
                    if point_after_operation < 0:
                        result_content += f"\nIn club [{club_name}] user [{real_name}] balance is [{previous_point}]" \
                                          f"\n Can't  decrease [{decreased_points}] point(s)"
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
                    result_content += f" \n for user [{real_name}] points in club [{club_name}] decreased " \
                                      f"by [{decreased_points}], " \
                                      f"now is [{point_after_operation}] "
                return result_content

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
                    result_content += f" \n for user [{real_name}] points in club [{club_name}] set to [{set_to_points}] "
                return result_content
            error_message = f"No valid operation."
            raise Exception(error_message)

        except Exception as e:
            error_message = f"Error in operate points :{e}"
            raise Exception(error_message)
        ...

    @staticmethod
    def consume_bonus_points(club_name: str,
                             operator_id: str, operator_name: str,
                             target_real_name: str,
                             consumed_points: int,
                             operator_real_name: str,
                             comments="",
                             ):
        try:
            result_content = f""
            club_room_id = ""
            previous_point = BonusManager.get_bonus_account(club_name=club_name, club_member_real_name=target_real_name) \
                .bonus_points_balance
            point_after_operation = previous_point - consumed_points
            if point_after_operation < 0:
                result_content += f"In club [{club_name}] user [{target_real_name}] balance is {previous_point}" \
                                  f"\n Can't afford to consume [{consumed_points}] point(s)"
                return result_content
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
            result_content += f"\nIn club [{club_name}], user [{target_real_name}] consumed [{consumed_points}] points." \
                              f"\nNow has [{point_after_operation}] left."
            return result_content

        except Exception as e:
            error_message = f" Error in consume points:{e}"
            raise Exception(error_message)
        ...

    @staticmethod
    def donate_bonus_points(club_name: str, club_member_real_name: str,
                            operator_id: str, operator_name: str, donated_points: int,
                            comments="",
                            ):
        try:
            result_content = f""
            club_room_id = ""
            common_account = BonusManager.get_bonus_account(club_name=club_name,
                                                            club_member_real_name=const_var.COMMON_ACCOUNT_REAL_NAME)
            source_account = BonusManager.get_bonus_account(club_name=club_name,
                                                            club_member_real_name=club_member_real_name)

            # source consume
            previous_point = source_account.bonus_points_balance
            point_after_operation = source_account.bonus_points_balance - donated_points
            if point_after_operation < 0:
                result_content += f"\nIn club [{club_name}] user [{club_member_real_name}] balance is {previous_point}" \
                                  f"\n Can't afford to donate [{donated_points}] point(s)"
                return result_content
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
            result_content += f"\nIn club [{club_name}], user [{club_member_real_name}] donated [{donated_points}] points." \
                              f"\nNow has [{point_after_operation}] left." \
                              f"\n Common user has [{common_points_after_operation}]"
            return result_content

        except Exception as e:
            error_message = f" Error in donate points: {e}"
            raise Exception(error_message)

    @staticmethod
    def query_bonus_points_balance(club_name: str, club_member_real_name: str):
        try:
            result_content = ""
            balance = BonusManager.get_bonus_account(club_name=club_name, club_member_real_name=club_member_real_name) \
                .bonus_points_balance
            result_content += f"\nIn club [{club_name}], user [{club_member_real_name}] has [{balance}] point(s) left"
            return result_content

        except Exception as e:
            error_message = f" Error in query points :{e}"
            raise Exception(error_message)
        ...

    @staticmethod
    def query_bonus_points_flow(club_name: str, club_member_real_name: str):
        try:
            result_content = ""
            existed_flows = db.table.session.query(db.BonusPointFlow) \
                .filter(db.BonusPointFlow.club_room_name == club_name) \
                .filter(db.BonusPointFlow.club_member_real_name == club_member_real_name) \
                .order_by(db.BonusPointFlow.bonus_flow_id.desc()) \
                .all()
            if len(existed_flows) <= 0:
                result_content += f"\nNo points flow for user [{club_member_real_name}] in club [{club_name}]"
                return result_content
            result_content += f"\\n <Points Flow>\n"
            for flow in existed_flows:
                result_content += f"\n flow_id {flow.bonus_flow_id}" \
                                  f"\n user {club_member_real_name}" \
                                  f"\n club {club_name}" \
                                  f"\n previous point(s) :{flow.previous_point}" \
                                  f"\n points after operation: {flow.point_after_operation}" \
                                  f"\n operator WeChat id: {flow.operator_id}" \
                                  f"\n operator WeChat name: {flow.operator_name}" \
                                  f"\n operator name : {flow.operator_real_name}" \
                                  f"\n operation date : {flow.operation_date}" \
                                  f"\n operation comments: {flow.bonus_flow_comments}\n"
            return result_content

        except Exception as e:
            error_message = f" Error in query point flow:{e}"
            raise Exception(error_message)

    @staticmethod
    def query_bonus_points_all(club_name: str):
        try:
            result_content = ""
            all_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
                order_by(db.BonusPoint.total_points.desc()).all()
            if len(all_bonus) <= 0:
                result_content += f"No any users for club [{club_name}] yet"
            count = 0
            result_content += f"\n club [{club_name}] collected points \n"
            for bonus in all_bonus:
                if bonus.club_member_real_name == const_var.COMMON_ACCOUNT_REAL_NAME:
                    continue
                count += 1
                result_content += f"\n #{count} user [{bonus.club_member_real_name}] " \
                                  f"collected points [{bonus.total_points}]"
            return result_content

        except Exception as e:
            error_message = f" :{e}"
            raise Exception(error_message)
        ...

    @staticmethod
    def query_balance_all(club_name: str):
        try:
            result_content = ""
            all_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
                order_by(db.BonusPoint.bonus_points_balance.desc()).all()
            if len(all_bonus) <= 0:
                result_content += f"No any users for club [{club_name}] yet"

            count = 0
            result_content += f"\n club [{club_name}] points balance \n"
            for bonus in all_bonus:
                count += 1
                result_content += f"\n #{count} user [{bonus.club_member_real_name}] " \
                                  f"points balance :[{bonus.bonus_points_balance}]"
            return result_content

        except Exception as e:
            error_message = f" :{e}"
            raise Exception(error_message)
        ...


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
            error_message = f"Activity title {title} doesn't exist"
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
            query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)
            if len(query.all()) > 0:
                error_message = f"{title} activity already existed, please consider update it"
                raise Exception(error_message)
            # bonus setting should be synced
            if point + max_earn_count + point_budget != 3 * const_var.DEFAULT_ACTIVITY_PARAS \
                    and point + max_earn_count + point_budget < 0:
                # != 3* defaults means, not all default
                # < 0 means any of them set  to default
                error_message = f"{title} activity points set error, please check again."
                raise Exception(error_message)
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
            result_content = f"Activity {title} created"
            return result_content
        except Exception as e:
            error_message = f"Error in update activity :{e}"
            raise Exception(error_message)

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
            result_content = ""
            activity = ClubActivityManager.get_activity(title)

            if description is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n description changed into {description}"
                activity.activity_description = description
            if planed_people is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n planed people changed from " \
                                  f"{activity.activity_planed_people} into {planed_people} "
                activity.activity_planed_people = planed_people
            if place is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n activity place changed from " \
                                  f"{activity.activity_place}  into {place} "
                activity.activity_place = place
            if point_budget is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n activity points budget changed from " \
                                  f"{activity.activity_point_budget} into {point_budget}"
                activity.activity_point_budget = point_budget
            if point is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"n activity points per check-in/joining changed from " \
                                  f"{activity.activity_point} into {point}"
                activity.activity_point = point
            if max_earn_count is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n activity max earn points changed from " \
                                  f"{activity.activity_max_count} to {max_earn_count}"
                activity.activity_max_count = max_earn_count
            if start_date is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n start date changed from {activity.activity_start_date} " \
                                  f"to {start_date}"
                activity.activity_start_date = start_date
            if end_date is not const_var.DEFAULT_ACTIVITY_PARAS:
                result_content += f"\n end date changed from {activity.activity_end_date} " \
                                  f"to {end_date}"
                activity.activity_end_date = end_date
            activity.activity_full_content += result_content
            # # if activity already existed,update it
            # query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title)

            db.table.session.commit()
            result_content += f"\nActivity {title} updated"
            return result_content
        except Exception as e:
            error_message = f"Error in update activity :{e}"
            raise Exception(error_message)

    @staticmethod
    def new_participates(title, partici_id, partici_name, partici_real_name, content):
        """
        :param title: activity title, as activity name is associated with club name, so no need for it
        :param partici_id: the participated wxid
        :param partici_name: the participated  nickname
        :param content: the activity participation content
        :param partici_real_name: real name
        :return:
        """
        try:
            result_content = ""
            # check activity status
            activity = ClubActivityManager.get_activity(title)

            activity_id = activity.activity_id
            # get end datetime from title
            activity_end_date = activity.activity_end_date
            if datetime.now() > activity_end_date:
                error_message = f"Activity {title} already timeout at {activity_end_date}"
                raise Exception(error_message)

            candidates_name = activity.activity_candidates_name.split(" ")
            if partici_real_name not in candidates_name:
                activity.activity_candidates += 1
                activity.activity_candidates_name += f" {partici_real_name}"
            # planed people handle
            left_seats = activity.activity_planed_people - activity.activity_candidates
            if activity.activity_planed_people != const_var.DEFAULT_ACTIVITY_PARAS:
                if left_seats < 0 and partici_real_name not in candidates_name:
                    error_message = f"No more activity seats. " \
                                    f"\nPlaned:{activity.activity_planed_people} " \
                                    f"\nTaken: {activity.activity_candidates} "
                    raise Exception(error_message)
                result_content += f"\nLeft Seats: [{left_seats}]"
            result_content += f" \n[{partici_real_name}] joined  activity [{title}]\n"

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
            )
            db.table.session.add(participates)
            db.table.session.commit()

            # bonus flow

            ## according title to check if we need to update bonus
            ## check if bonus set in this activity
            if activity.activity_point == const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_max_count == const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_point_budget == const_var.DEFAULT_ACTIVITY_PARAS \
                    :
                db.table.session.commit()
                return result_content

            ## if no more budget
            if activity.activity_consumed_budget + activity.activity_point > activity.activity_point_budget:
                db.table.session.commit()
                result_content += f" \n [No more points budget, can't increase your points]" \
                                  f" \n Activity points budget: {activity.activity_point_budget} " \
                                  f" \n Activity consumed points: {activity.activity_consumed_budget} "
                return result_content

            ## if already reached max earned points

            # PS: the last one, is current operating one, for
            current_flow = db.table.session.query(db.ClubActivityFlow) \
                .filter(db.ClubActivityFlow.activity_id == activity.activity_id) \
                .filter(db.ClubActivityFlow.activity_participates_real_name == partici_real_name) \
                .order_by(db.ClubActivityFlow.activity_flow_id.desc()) \
                .first()
            if all_previous_earned + activity.activity_point > activity.activity_max_count:
                current_flow.activity_point_earned = all_previous_earned
                result_content += f" \n [Already reached max points in current activity] " \
                                  f" \n [Max]: {activity.activity_max_count} " \
                                  f" \n [Earned]: {all_previous_earned}"
                db.table.session.commit()
                return result_content
            # can add points
            current_flow.activity_point_earned += activity.activity_point

            # new bonus flow
            previous_point_balance = BonusManager.get_bonus_account(club_name=activity.club_room_name,
                                                                    club_member_real_name=partici_real_name) \
                .total_points
            comments = f"Joined activity {title} "
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
            result_content += f" \n [{activity.activity_point}] point(s) added " \
                              f" \n activity points now have " \
                              f"{activity.activity_point_budget - activity.activity_consumed_budget} left" \
                              f" \n In [{activity.club_room_name}] club " \
                              f"user [{partici_real_name}] already collected " \
                              f"[{bonus_account.total_points}] " \
                              f" \n current balance:[{bonus_account.bonus_points_balance}]"
            db.table.session.commit()
            return result_content
        except Exception as e:
            db.table.session.commit()
            error_message = f"Error in new participates: {e}"
            raise Exception(error_message)

    @staticmethod
    def show_activity_status(title, show_flag: int = 1):
        """
        :param title:
        :param show_flag, 1-> name, 2-> date, 4-> content, 8(TODO)-> name,date,content,points change
        :return:
        """
        try:
            activity = ClubActivityManager.get_activity(title)
            activity_id = activity.activity_id

            existed = db.table.session.query(db.ClubActivityFlow). \
                filter(db.ClubActivityFlow.activity_id == activity_id).all()
            if len(existed) <= 0:
                error_message = f"activity flow {title} doesn't exist"
                raise Exception(error_message)
            result = f"\nActivity Title:{title}\n"
            count = 0
            for flow in existed:
                result += "\n"
                count += 1
                result += f"\n#{count}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_NAME:  # name
                    result += f"\nnickname:{flow.activity_participates_real_name}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_DATE:  # date
                    result += f"\ndate:{flow.activity_flow_creat_date}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_CONTENT:  # content
                    result += f"\ncontent:\n[{flow.activity_flow_content}]"
            return result
        except Exception as e:
            error_message = f"Error in show activity status: {e}"
            raise Exception(error_message)
