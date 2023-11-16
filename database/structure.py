from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column, Integer, Text, ForeignKey, Double
from .conn_settings import psqlstr


engine = create_engine(psqlstr)
data = MetaData()
conn = engine.connect()

heroes = Table('heroes', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False)
)

categories = Table('categories', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False),
    Column('cover_img', Text, nullable=True)
)

product_types = Table('product_types', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False)
)

clients = Table('clients', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('phone', Text, nullable=False),
    Column('description', Text, nullable=False)
)

identities = Table('identities', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('name', Text, nullable=False),
    Column('hero_id', ForeignKey('heroes.id')),
    Column('product_type_id', ForeignKey('product_type.id')),
    Column('category_id', ForeignKey('categories.id')),
    Column('description', Text, nullable=False),
    Column('img_path', Text, nullable=False),
    Column('art', Text, nullable=False, unique=True),
)

items = Table('items', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('identity_id', ForeignKey('identity.id')),
    Column('size', Text, nullable=False),
    Column('price', Double, nullable=False)
)

categories_to_types = Table('categories_to_types', data,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column('category_id', ForeignKey('categories.id')),
    Column('product_type_id', ForeignKey('product_types.id'))
)

refresh_tokens = Table('refresh_tokens', data,
    Column("id", Text, primary_key=True, unique=True)
)