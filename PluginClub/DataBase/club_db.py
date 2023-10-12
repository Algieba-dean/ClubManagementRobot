from pathlib import Path

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, scoped_session

Base = declarative_base()


class ClubActivity(Base):
    __tablename__ = "ClubActivity"
    activity_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)

    club_room_id = Column(String(50))  # club WeChat room id
    club_room_name = Column(String(512))  # club WeChat room name

    activity_title = Column(String(1024), unique=True)  # unique activity name
    activity_description = Column(String(1024 * 100))
    activity_full_content = Column(String(1024 * 100))  # full description of one activity

    activity_organizer_id = Column(String(100))  # initializer WeChat id
    activity_organizer_name = Column(String(100))  # initializer WeChat name
    activity_organizer_real_name = Column(String(100))  # initializer real name, seems no need

    activity_create_date = Column(DateTime)  # the activity create date
    activity_regis_start_date = Column(DateTime)  # register start date,  seems no need
    activity_regis_end_date = Column(DateTime)  # register end date,  seems no need
    activity_start_date = Column(DateTime)  # activity start date
    activity_end_date = Column(DateTime)  # activity end date

    activity_place = Column(String(512))  # online or other place, default is empty
    activity_day_point_join_count = Column(Integer) # max with-point join count in a day
    activity_planed_people = Column(Integer)  # planed how many people can join in
    activity_candidates = Column(Integer)  # already registered candidates
    activity_candidates_name = Column(String(1024 * 100))  # already registered candidates
    activity_point_budget = Column(Integer)  # planed points for this activity
    activity_consumed_budget = Column(Integer)  # after activity finished, how many budget costed , seems no need
    activity_point = Column(Integer)  # for every joined, how much point can earn
    activity_max_count = Column(Integer)  # Max count to take part in this single activity


class ClubActivityFlow(Base):
    __tablename__ = "ClubActivityFlow"
    activity_flow_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    activity_flow_content = Column(String(1024 * 100))
    activity_id = Column(Integer, ForeignKey("ClubActivity.activity_id"))
    activity_participates_id = Column(String(1024))
    activity_participates_name = Column(String(1024))
    activity_participates_real_name = Column(String(1024))
    activity_point_earned = Column(Integer) # this is for all earned in this activity
    this_time_earned_point = Column(Integer) # this is for this flow
    bonus_point_flow_id = Column(Integer)
    activity_flow_creat_date = Column(DateTime)
    join_comments = Column(String(1024 * 100))

    activity = relationship("ClubActivity", backref="ClubActivityFlow")


class BonusPoint(Base):
    __tablename__ = "BonusPoint"
    bonus_point_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    club_room_name = Column(String(512))
    club_member_real_name = Column(String(50))
    bonus_points_balance = Column(Integer)
    total_points = Column(Integer)  # transferred points won't be here
    related_change_flow_ids = Column(String(1024 * 10))
    last_changed_flow_id = Column(Integer)


class BonusPointFlow(Base):
    __tablename__ = "BonusPointFlow"
    bonus_flow_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    club_member_real_name = Column(String(50))
    bonus_point_id = Column(Integer)  # the related people bonus id
    club_room_id = Column(String(50))
    club_room_name = Column(String(512))
    bonus_flow_type = Column(Integer)  # 0->increase , 1->decrease, 2-> force update

    operator_id = Column(String(50))  # people who did this bonus change
    operator_name = Column(String(512))  # people who did this bonus change
    operator_real_name = Column(String(512))  # people who did this bonus change
    operation_date = Column(DateTime)

    activity_flow_id = Column(Integer)
    previous_point = Column(Integer)
    point_after_operation = Column(Integer)
    bonus_flow_comments = Column(String(1024))


class TableManager:
    def __init__(self):
        self.db_path = Path("club.db")
        self.engine = create_engine('sqlite:///club.db',
                                    # echo=True,
                                    max_overflow=0,
                                    pool_size=5,
                                    pool_timeout=10,
                                    pool_recycle=1)

        if not self.db_path.exists():
            self.create_tables()
        self.session = scoped_session(sessionmaker(bind=self.engine))

    def create_tables(self):
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)


table = TableManager()

# table.drop_tables()
# table.create_tables()
