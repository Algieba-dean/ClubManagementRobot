from datetime import datetime, timedelta

import PluginClub.DataBase.club_db as db
from club_activity import ClubActivityManager

test_room_id = "123@chatroom"
test_room_name = "test room"
test_title = "Activity01"
test_organizer_id = "wxid001"
test_organizer_name = "001"
test_description = "a"
test_full_content = "aa" * 100
test_start_date = datetime.now()
test_end_date = datetime.now() + timedelta(days=3)
test_planed_people = 10
test_place = "earth"
test_point = 3
test_max_earn_point = 27
test_point_budget = 270


def test_new_activity_success():
    db.table.create_tables()

    # test new activity
    result = ClubActivityManager.new_activity(room_id=test_room_id,
                                              room_name=test_room_name,
                                              title=test_title,
                                              full_content=test_full_content,
                                              organizer_id=test_organizer_id,
                                              organizer_name=test_organizer_name,
                                              description=test_description,
                                              start_date=test_start_date,
                                              planed_people=test_planed_people,
                                              place=test_place,
                                              point=test_point,
                                              point_budget=test_point_budget,
                                              max_earn_count=test_max_earn_point,
                                              end_date=test_end_date)
    print(result)


def test_update_activity_success():
    # test new activity
    test_new_activity_success()
    end_date = test_end_date + timedelta(days=4)

    # test update activity
    result = ClubActivityManager.update_activity(title=test_title, end_date=end_date)

    query = db.table.session.query(db.ClubActivity).filter(db.ClubActivity.activity_title == test_title).first()
    print(query.activity_full_content)
    print(query.activity_planed_people)
    print(result)


def test_update_activity_wrong():
    end_date = test_end_date + timedelta(days=4)
    test_new_activity_success()
    # test update wrong activity
    try:
        result = ClubActivityManager.update_activity(title=test_title + "1",
                                                     end_date=end_date)
        print(result)
    except Exception as e:
        print(e)


def test_join_activity_success():

    test_new_activity_success()
    # test join activity
    for i in range(10):
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        partici_real_name = f"real_name{i}"
        content = "test Content \n" * (i + 1)

        result = ClubActivityManager.new_participates(title=test_title,
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      partici_real_name=partici_real_name,
                                                      content=content,
                                                      )
        print(result)
        ...


def test_join_activity_no_seats():
    test_new_activity_success()
    # test join activity
    for i in range(11):
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        partici_real_name = f"real_name{i}"
        content = "test Content \n" * (i + 1)

        try:
            result = ClubActivityManager.new_participates(title=test_title,
                                                          partici_id=partici_id,
                                                          partici_name=partici_name,
                                                          partici_real_name=partici_real_name,
                                                          content=content,
                                                          )
            print(result)

        except Exception as e:
            print(e)
    ...


def test_no_point_budget():
    test_new_activity_success()
    ClubActivityManager.update_activity(title=test_title, point_budget=30)
    # test join activity
    for i in range(10):
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        partici_real_name = f"real_name{i}"
        content = "test Content \n" * (i + 1)

        result = ClubActivityManager.new_participates(title=test_title,
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      partici_real_name=partici_real_name,
                                                      content=content,
                                                      )
        print(result)
    try:
        result = ClubActivityManager.new_participates(title=test_title,
                                                      partici_id="wxid001 ",
                                                      partici_name="001",
                                                      partici_real_name="real_name0",
                                                      content="aaabbb",
                                                      )
        print(result)

    except Exception as e:
        print(e)


def test_beyond_max_per_person():
    test_new_activity_success()
    ClubActivityManager.update_activity(title=test_title, point_budget=30)
    # test join activity
    for i in range(10):
        partici_id = f"wxid00"
        partici_name = f"00"
        partici_real_name = f"real_name"
        content = "test Content \n" * (i + 1)

        try:
            result = ClubActivityManager.new_participates(title=test_title,
                                                          partici_id=partici_id,
                                                          partici_name=partici_name,
                                                          partici_real_name=partici_real_name,
                                                          content=content,
                                                          )
            print(result)
        except Exception as e:
            print(e)


def test_join_activity_wrong_title():
    test_new_activity_success()
    # test join wrong activity

    try:
        i = 99
        partici_id = f"wxid00{i}"
        partici_name = f"00{i}"
        content = "test Content \n"

        result = ClubActivityManager.new_participates(title=test_title + "0",
                                                      partici_id=partici_id,
                                                      partici_name=partici_name,
                                                      content=content
                                                      )
        print(result)
    except Exception as e:
        print(e)


def test_show_activity_status():
    # test new activity
    test_new_activity_success()
    result = ClubActivityManager.show_activity_status(title=test_title, show_flag=1)
    result = ClubActivityManager.show_activity_status(title=test_title, show_flag=1)
    print(result)
    result = ClubActivityManager.show_activity_status(title=test_title, show_flag=3)
    print(result)
    result = ClubActivityManager.show_activity_status(title=test_title, show_flag=7)
    print(result)


if __name__ == "__main__":
    ...

    # test_new_activity_success()
    # test_update_activity_success()
    # test_join_activity_success()
    # test_join_activity_no_seats()
    # test_no_point_budget()
    test_beyond_max_per_person()
