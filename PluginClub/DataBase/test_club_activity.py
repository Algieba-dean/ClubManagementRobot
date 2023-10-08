from datetime import datetime, timedelta

import PluginClub.DataBase.club_db as db
from club_activity import ClubActivityManager, BonusManager

# activity test
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

# bonus test
test_club_name = test_room_name
test_operator_id = test_organizer_id
test_target_real_name = test_organizer_name
test_operator_real_name = test_target_real_name
test_comments = "Test"
test_target_names = [str(i) for i in range(10)]
test_target_name = ["1", ]
test_target_real_name = "1"


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


def test_update_activity_title_wrong():
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
        partici_real_name = f"{i}"
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


def test_operate_points():
    # test_new_activity_success()
    range_ = 5
    increased_points = "2"
    decreased_points = "3"
    print("\n\n--------increase test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_name,
                                                   increased_points=increased_points)
        print(result)

    print("\n\n--------increase test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_name,
                                                   decreased_points=decreased_points)
        print(result)
    print("\n\n--------set to test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_name,
                                                   set_to_points=str(i))
        print(result)


def test_operate_multi_user_points():
    range_ = 5
    increased_points = "2"
    decreased_points = "3"
    print("\n\n--------increase test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_names,
                                                   increased_points=increased_points)
        print(result)

    print("\n\n--------increase test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_names,
                                                   decreased_points=decreased_points)
        print(result)
    print("\n\n--------set to test---------")
    for i in range(range_):
        result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   operator_real_name=test_operator_real_name,
                                                   target_real_names=test_target_names,
                                                   set_to_points=str(i))
        print(result)
    ...


def test_consume_points():
    range_ = 5
    result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                               operator_id=test_operator_id,
                                               operator_name=test_operator_id,
                                               operator_real_name=test_operator_real_name,
                                               target_real_names=test_target_name,
                                               set_to_points="9",
                                               comments="set to 9")
    for i in range(range_):
        result = BonusManager.consume_bonus_points(club_name=test_room_name,
                                                   operator_id=test_operator_id,
                                                   operator_name=test_operator_id,
                                                   target_real_name=test_target_real_name,
                                                   consumed_points=2,
                                                   operator_real_name=test_operator_real_name,
                                                   comments="Buy pens"
                                                   )
        print(result)


def test_donate_points():
    range_ = 5
    result = BonusManager.operate_bonus_points(club_name=test_room_name,
                                               operator_id=test_operator_id,
                                               operator_name=test_operator_id,
                                               operator_real_name=test_operator_real_name,
                                               target_real_names=test_target_name,
                                               set_to_points="7",
                                               comments="Set to 7")
    for i in range(range_):
        result = BonusManager.donate_bonus_points(club_name=test_room_name,
                                                  operator_id=test_operator_id,
                                                  operator_name=test_operator_id,
                                                  donated_points=2,
                                                  club_member_real_name=test_target_real_name,
                                                  comments="Donate"
                                                  )
        print(result)


def test_query_bonus_points_balance():
    result = BonusManager.query_bonus_points_balance(club_name=test_room_name,
                                                     club_member_real_name=test_target_real_name)
    print(result)
    ...


def test_query_bonus_points_flow():
    result = BonusManager.query_bonus_points_flow(club_name=test_room_name,
                                                  club_member_real_name=test_target_real_name)
    print(result)
    ...


def test_query_bonus_points_all():
    result = BonusManager.query_bonus_points_all(club_name=test_room_name)
    print(result)
    ...


def test_query_balance_all():
    result = BonusManager.query_balance_all(club_name=test_room_name)
    print(result)
    ...


if __name__ == "__main__":
    ...

    # test_new_activity_success()
    # test_update_activity_success()
    # test_join_activity_success()
    test_join_activity_no_seats()
    # test_no_point_budget()
    # test_beyond_max_per_person()

    # test_operate_points()
    # test_operate_multi_user_points()
    # test_consume_points()
    # test_donate_points()
    # test_query_bonus_points_balance()
    # test_query_bonus_points_flow()
    # test_query_bonus_points_all()
    # test_query_balance_all()
