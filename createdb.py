from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean
engine = create_engine('sqlite:///rsvp.db', echo = True)
meta = MetaData()

invitation = Table(
    'invitation', meta,
    Column('pid', Integer, primary_key=True),
    Column('group_name', String),
    Column('guest_name', String, primary_key=True),
    Column('diet', String),
    Column('isConfirmed', Boolean),
    )

extras = Table(
    'extras', meta,
    Column('pid', Integer, primary_key=True),
    Column('music_choice_1', String),
    Column('music_choice_2', String),
    Column('music_choice_3', String),
    Column('shuttle_service', Boolean),
    Column('special_wishes', String),
    )

meta.create_all(engine)