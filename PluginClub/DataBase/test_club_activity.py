from datetime import datetime, timedelta

import PluginClub.DataBase.club_db as db
from club_activity import ClubActivityManager


def test_new_activity_success():
    db.table.create_tables()
    room_id = "123@chatroom"
    room_name = "test room"
    title = "Activity01"
    organizer_id = "wxid001"
    organizer_name = "001"
    description = "a"
    full_content = "aa" * 100
    start_date = datetime.now()
    end_date = datetime.now() + timedelta(days=3)
    planed_people = 10
    place = "earth"
    point = 3
    max_earn_point = 27
    point_budget = 270

    # test new activity
    result = ClubActivityManager.new_activity(room_id=room_id,
                                              room_name=room_name,
                                              title=title,
                                              full_content=full_content,
                                              organizer_id=organizer_id,
                                              organizer_name=organizer_name,
                                              description=description,
                                              start_date=start_date,
                                              planed_people=planed_people,
                                              place=place,
                                              point=point,
                                              point_budget=point_budget,
                                              max_earn_count=max_earn_point,
                                              end_date=end_date)
    print(result)


def test_update_activity_success():
    title = "Activity01"
    # test new activity
    test_new_activity_success()
    end_date = datetime.now() + timedelta(days=4)

    # test update activity
    result = ClubActivityManager.update_activity(title=title, end_date=end_date)

    query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == title).first()
    print(query.activity_full_content)
    print(query.activity_planed_people)
    print(result)


def test_update_activity_wrong():
    title = "Activity01"
    end_date = datetime.now() + timedelta(days=4)
    test_new_activity_success()
    # test update wrong activity
    try:
        result = ClubActivityManager.update_activity(title=title + "1",
                                                     end_date=end_date)
        print(result)
    except Exception as e:
        print(e)


def test_join_activity_success():
    title = "Activity01"

    test_new_activity_success()
    # test join activity
    for i in range(11):
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        partici_real_name = f"real_name{i}"
        content = "test Content \n" * (i + 1)

        result = ClubActivityManager.new_participates(title=title,
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      partici_real_name=partici_real_name,
                                                      content=content,
                                                      )
        print(result)
        ...


def test_join_activity_wrong():
    title = "Activity01"

    test_new_activity_success()
    # test join wrong activity

    try:
        i = 99
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        content = "test Content \n"

        result = ClubActivityManager.new_participates(title=title + "0",
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      content=content
                                                      )
        print(result)
    except Exception as e:
        print(e)


def test_show_activity_status():
    title = "Activity01"

    # test new activity
    test_new_activity_success()
    result = ClubActivityManager.show_activity_status(title=title, show_flag=1)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=1)
    print(result)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=3)
    print(result)
    result = ClubActivityManager.show_activity_status(title=title, show_flag=7)
    print(result)


if __name__ == "__main__":
    ...

    # test_new_activity_success()
    # test_update_activity_success()
    # test_join_activity_success()
