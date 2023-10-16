from datetime import datetime,date

import PluginClub.DataBase.club_db as db
from PluginClub.DataBase import const_var
from PluginClub.DataBase.club_utils import OutputMessageIterator
from PluginClub.DataBase.club_command_helper import CommandHelper
from PluginClub.DataBase.club_bonus_manager import BonusManager


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
                     point_join_max_count_per_day,
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
                activity_day_point_join_count=point_join_max_count_per_day,
                activity_start_date=start_date,
                activity_end_date=end_date,
                activity_candidates=0,
                activity_candidates_name="",
                activity_consumed_budget=0,
            )
            db.table.session.add(activity)
            db.table.session.commit()
            output_message = f"发起活动[{title}]成功,如需打卡请参考以下命令"
            output.add_new_message(output_message)
            example_message = CommandHelper.get_new_participants_example() \
                .replace(const_var.HELPER_ACTIVITY_NAME, title)
            output.add_new_message(example_message)
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"发起活动时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_new_activity_example() \
                .replace(const_var.HELPER_ACTIVITY_NAME, title)
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
                        point_join_max_count_per_day=const_var.DEFAULT_ACTIVITY_PARAS,
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

            if description is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and description != activity.activity_description:
                output_message += f"活动描述更新为: [{description}]"
                activity.activity_description = description
            if planed_people is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and planed_people != activity.activity_planed_people:
                output_message += f"\n活动人数限制从" \
                                  f"[{activity.activity_planed_people}]更新为[{planed_people}]"
                activity.activity_planed_people = planed_people
            if place is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and place != activity.activity_place:
                output_message += f"\n活动地点从" \
                                  f"[{activity.activity_place}]更新为[{place}]"
                activity.activity_place = place
            if point_budget is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_point_budget != point_budget:
                output_message += f"\n活动积分预算从" \
                                  f"[{activity.activity_point_budget}]更新为[{point_budget}]"
                activity.activity_point_budget = point_budget
            if point is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_point != point:
                output_message += f"\n单次参与/打卡积分奖励从" \
                                  f"[{activity.activity_point}]更新为[{point}]"
                activity.activity_point = point
            if point_join_max_count_per_day is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and activity.activity_day_point_join_count != point_join_max_count_per_day:
                output_message += f"\n单日可积分打卡次数从" \
                                  f"[{activity.activity_day_point_join_count}]更新为[{point_join_max_count_per_day}]"
                activity.activity_day_point_join_count = point_join_max_count_per_day
            if max_earn_count is not const_var.DEFAULT_ACTIVITY_PARAS \
                    and max_earn_count != activity.activity_max_count:
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
            example_message = CommandHelper.get_update_activity_example() \
                .replace(const_var.HELPER_ACTIVITY_NAME, title)
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
            # check if activity started
            activity_start_date = activity.activity_start_date
            if datetime.now() < activity_start_date:
                error_message = f"活动[{title}]将于[{activity_start_date}]开始，请在活动开始后进行再次进行参与"
                raise Exception(error_message)
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
            output_message += f" \n用户[{partici_real_name}]" \
                              f"\n参与活动[{title}] 成功\n"

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
                this_time_earned_point=0,
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

            today_earned_counts = 0
            ## if max in one day
            if activity.activity_day_point_join_count != const_var.DEFAULT_ACTIVITY_PARAS:
                today = date.today()
                today_start = today.strftime("%Y-%m-%d") + " 00:00:00"
                today_end = today.strftime("%Y-%m-%d") + " 23:59:59"
                today_earned_flows = db.table.session.query(db.ClubActivityFlow) \
                    .filter(db.ClubActivityFlow.activity_id == activity.activity_id) \
                    .filter(db.ClubActivityFlow.activity_participates_real_name == partici_real_name) \
                    .filter(db.ClubActivityFlow.activity_flow_creat_date.between(today_start,today_end)) \
                    .filter(db.ClubActivityFlow.this_time_earned_point > 0) \
                    .order_by(db.ClubActivityFlow.activity_flow_id.desc()) \
                    .all()
                # as today's flow earned point is 0, so it's fine to query after it
                today_earned_counts = len(today_earned_flows)
                if today_earned_counts >= activity.activity_day_point_join_count:
                    db.table.session.commit()
                    output_message = f" 您在该活动中已达到单日可积分打卡上限,本次打卡不增加积分" \
                                     f" \n活动单日可积分打卡次数: {activity.activity_day_point_join_count} " \
                                     f" \n今日已积分打卡次数: {today_earned_counts} "
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
                                 f" \n 已获得积分的打卡次数: {int(all_previous_earned / activity.activity_point)}"
                db.table.session.commit()
                output.add_new_message(output_message)
                return output
            # can add points
            current_flow.activity_point_earned += activity.activity_point
            current_flow.this_time_earned_point = activity.activity_point

            # new bonus flow
            previous_point_balance = BonusManager.get_bonus_account(club_name=activity.club_room_name,
                                                                    club_member_real_name=partici_real_name) \
                .total_points
            comments = f"活动[{title}] 打卡成功"
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
            output_message = f"\n新增积分[{activity.activity_point}]" \
                             f"\n在俱乐部群[{activity.club_room_name}]积分账户中" \
                             f"\n用户[{partici_real_name}]累计获得的总积分为: " \
                             f"[{bonus_account.total_points}] " \
                             f"\n目前积分余额为: [{bonus_account.bonus_points_balance}]"
            if activity.activity_point_budget != const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n目前活动剩余积分预算为[{activity.activity_point_budget - activity.activity_consumed_budget}]"
            if activity.activity_day_point_join_count != const_var.DEFAULT_ACTIVITY_PARAS:
                output_message += f"\n今日活动可积分打卡次数剩余[{activity.activity_day_point_join_count - today_earned_counts -1}]"
            output.add_new_message(output_message)
            db.table.session.commit()
            return output
        except Exception as e:
            output = OutputMessageIterator()
            error_message = f"打卡时出现错误 :{e} \n 请参考以下示例重试."
            output.add_new_message(error_message)
            example_message = CommandHelper.get_new_participants_example() \
                .replace(const_var.HELPER_ACTIVITY_NAME, title)
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
            output.add_new_message(result)
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
            example_message = CommandHelper.get_check_activity_status_example() \
                .replace(const_var.HELPER_ACTIVITY_NAME, title)
            output.add_new_message(example_message)
            return output
