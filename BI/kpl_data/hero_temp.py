# 使用sqlalchemy 插入英雄
from sqlalchemy import Column, String, Integer, Float, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()
# 定义Hero对象:
class Hero(Base):
    # 表的名字:
    __tablename__ = 'hero_temp'
     # 表的结构:
    hero_id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer)
    hero_name = Column(String(255))
    height = Column(Float(3,2))

engine = create_engine('mysql+mysqlconnector://root:passw0rdcc4@localhost:3306/wucai')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建session对象:
session = DBSession()
# 创建Hero对象:
new_hero = Hero(hero_id = 1001, hero_name = "张飞", height = 2.08)
# 添加到session:
session.add(new_hero)
# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()
