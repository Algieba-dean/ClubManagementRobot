from datetime import datetime

import PluginClub.DataBase.club_db as db
from PluginClub.DataBase import const_var
from PluginClub.DataBase.club_command_helper import CommandHelper
from PluginClub.DataBase.club_utils import OutputMessageIterator


class BonusManager:
    @staticmethod
    def get_bonus_account(club_name, club_member_real_name, create_account_if_new=True):
        """
        # return bonus account query result, if no bonus account, will create one.
        :param club_name:
        :param club_member_real_name:
        :return:
        """
        existed_bonus = db.table.session.query(db.BonusPoint).filter(db.BonusPoint.club_room_name == club_name). \
            filter(db.BonusPoint.club_member_real_name == club_member_real_name).all()
        if len(existed_bonus) <= 0:
            if not create_account_if_new:
                error_message = f"在俱乐部群[{club_name}]积分记录中，不存在用户[{club_member_real_name}]"
                raise Exception("")
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
            example_message = CommandHelper.get_operate_points_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
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
            output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"消费积分时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_consume_points_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
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
            example_message = CommandHelper.get_donate_points_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
            output.add_new_message(example_message)
            return output

    @staticmethod
    def query_bonus_points_balance(club_name: str, club_member_real_name: str):
        try:
            output_message = ""
            output = OutputMessageIterator()
            balance = BonusManager.get_bonus_account(club_name=club_name,
                                                     club_member_real_name=club_member_real_name,
                                                     create_account_if_new=False) \
                .bonus_points_balance
            output_message += f"在俱乐部群[{club_name}]积分记录中,用户[{club_member_real_name}]积分余额为[{balance}]"
            output.add_new_message(output_message)
            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分余额时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_balance_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
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
                error_message = f"\n在俱乐部群[{club_name}]积分记录中用户[{club_member_real_name}]无积分流水记录"
                raise Exception(error_message)
            output_message += f"<积分流水>" \
                              f"\n用户名: [{club_member_real_name}]" \
                              f"\n俱乐部群名:[{club_name}]"
            output.add_new_message(output_message)
            count = 0
            output_message = ""
            for flow in existed_flows:
                count += 1
                output_message += f"\n序号#{count}" \
                                  f"\n流水ID#{flow.bonus_flow_id}" \
                                  f"\n操作前积分:{flow.previous_point}" \
                                  f"\n操作后积分: {flow.point_after_operation}" \
                                  f"\n操作人微信ID: {flow.operator_id}" \
                                  f"\n操作人微信昵称: {flow.operator_name}" \
                                  f"\n操作用户: {flow.operator_real_name}" \
                                  f"\n操作执行日期: {flow.operation_date}" \
                                  f"\n操作备注: {flow.bonus_flow_comments}\n"
                if count % output_counts_per_message == 0:
                    output.add_new_message(output_message)
                    output_message = ""
            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)

            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分流水时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_flow_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
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
                output_message += f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                  f"累计获得积分: [{bonus.total_points}]"
                if count % output_counts_per_message == 0:
                    output.add_new_message(output_message)
                    output_message = ""
            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)

            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分总榜时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_points_all_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
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
                output_message += f"\n#{count} 用户[{bonus.club_member_real_name}] " \
                                  f"积分余额: [{bonus.bonus_points_balance}]"
                if count % output_counts_per_message == 0:
                    output.add_new_message(output_message)
                    output_message = ""
            if count % output_counts_per_message != 0:
                output.add_new_message(output_message)

            return output

        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"查询积分余额榜时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_query_balance_all_example() \
                .replace(const_var.HELPER_CLUB_GROUP_NAME, club_name)
            output.add_new_message(example_message)
            return output
