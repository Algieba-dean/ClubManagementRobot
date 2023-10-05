from datetime import datetime

import PluginClub.DataBase.club_db as db
import const_var


class ClubActivityManager:

    @staticmethod
    def new_activity(room_id, room_name, title, full_content, description,
                     organizer_id, organizer_name,
                     planed_people,
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
                activity_candidates=0,
                activity_start_date=start_date,
                activity_planed_people=planed_people,
                activity_end_date=end_date,
            )
            db.table.session.add(activity)
            db.table.session.commit()
            result_content = f"Activity {title} created"
            return result_content
        except Exception as e:
            error_meesage = f"Error in update activity :{e}"
            raise Exception(error_meesage)

    @staticmethod
    def update_activity(
            title,
            room_id=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            room_name=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            full_content=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            description=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            organizer_id=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            organizer_name=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            planed_people=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            start_date=const_var.NOT_CHANGED_ACTIVITY_PARAS,
            end_date=const_var.NOT_CHANGED_ACTIVITY_PARAS,
    ):
        """
        PS: only title and target optional must be here
        :param room_id: room id
        :param room_name: the name of room
        :param full_content: full activity content
        :param description
        :param title: activity title
        :param organizer_id: the wxid of organizer
        :param organizer_name: the nickname of organizer
        :param planed_people: planed people of an activity
        :param start_date: type is datetime, the first day of activity
        :param end_date: type is datetime, the last day of activity
        :return:
        """
        try:
            ## check title correct
            result_content = ""
            existed = db.table.session.query(db.ClubActivity, ). \
                filter(db.ClubActivity.activity_title == title).all()
            if not existed:
                error_message = f"Error in new participates: Activity name {title} doesn't exist"
                raise Exception(error_message)
            # get activity id from title
            activity = existed[0]
            activity_id = activity.activity_id

            if room_id is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
                result_content += f"\n room id changed into {room_id}"
                activity.club_room_id = room_id
            if room_name is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
                result_content += f"\n room name changed into {room_name}"
                activity.club_room_name = room_name
            if description is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
                result_content += f"\n description changed into {description}"
                activity.activity_description = description
            if planed_people is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
                result_content += f"\n planed people changed from " \
                                  f"{activity.activity_planed_people} into {planed_people} "
                activity.activity_planed_people = planed_people
            if start_date is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
                result_content += f"\n start date changed from {activity.activity_start_date} " \
                                  f"to {start_date}"
                activity.activity_start_date = start_date
            if end_date is not const_var.NOT_CHANGED_ACTIVITY_PARAS:
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
            ## check title correct
            existed = db.table.session.query(db.ClubActivity, ). \
                filter(db.ClubActivity.activity_title == title).all()
            if not existed:
                error_message = f"Error in new participates: Activity name {title} doesn't exist"
                raise Exception(error_message)
            # get activity id from title
            activity = existed[0]
            activity_id = activity.activity_id
            # get end datetime from title
            activity_end_date = activity.activity_end_date
            if datetime.now() > activity_end_date:
                error_message = f"Error in new participates: Activity {title} already timeout at {activity_end_date}"
                raise Exception(error_message)

            # planed people handle
            left_seats = activity.activity_planed_people - activity.activity_candidates
            if activity.activity_planed_people != const_var.DEFAULT_OPTION_FLAG:
                if left_seats <= 0:
                    error_message = f"Error in new participates: No more activity seats. " \
                                    f"\nPlaned:{activity.activity_planed_people} " \
                                    f"\nTaken: {activity.activity_candidates} "
                    raise Exception(error_message)
                result_content += f"Left Seats: {left_seats - 1}\n"
            result_content += f"\nActivity {title} Joined\n"
            activity.activity_candidates += 1

            # activity flow

            participates = db.ClubActivityFlow(
                activity_flow_content=content,
                activity_id=activity_id,
                activity_participates_id=partici_id,
                activity_participates_name=partici_name,
                activity_participates_real_name=partici_real_name,
                activity_flow_creat_date=datetime.now(),
            )
            db.table.session.add(participates)
            db.table.session.commit()

            # bonus flow

            ## check if bonus setted in this activity

            return result_content
        except Exception as e:
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
            existed = db.table.session.query(db.ClubActivity, ). \
                filter(db.ClubActivity.activity_title == title).first()
            activity_id = existed.activity_id
            if not existed:
                error_message = f"Error in show activity status: activity {title} doesn't exist"
                raise Exception(error_message)
            existed = db.table.session.query(db.ClubActivityFlow). \
                filter(db.ClubActivityFlow.activity_id == activity_id).all()
            if not existed:
                error_message = f"Error in show activity status: activity flow {title} doesn't exist"
                raise Exception(error_message)
            result = f"\nActivity Title:{title}"
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
