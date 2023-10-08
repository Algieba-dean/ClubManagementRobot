from datetime import datetime

import PluginClub.DataBase.club_db as db
import const_var


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
            error_message = f" :{e}"
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
            for flow in existed:
                result += "\n"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_NAME:  # name
                    result += f"nickname:{flow.activity_participates_name}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_DATE:  # date
                    result += f"\ndate:{flow.activity_flow_creat_date}"
                if show_flag & const_var.SHOW_ACTIVITY_STATUS_CONTENT:  # content
                    result += f"\ncontent:\n[{flow.activity_flow_content}]"
            return result
        except Exception as e:
            error_message = f"Error in show activity status: {e}"
            raise Exception(error_message)
