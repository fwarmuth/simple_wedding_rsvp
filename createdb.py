from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Boolean
engine = create_engine('sqlite:///rsvp.db', echo = True)
meta = MetaData()

invitation = Table(
    'invitation', meta,
    Column('pid', Integer, primary_key=True),
    Column('name', String, primary_key=True),
    Column('diet', String),
    Column('isConfirmed', Boolean),
    )

meta.create_all(engine)