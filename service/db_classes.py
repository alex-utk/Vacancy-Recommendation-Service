import re
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, \
                       String, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase): pass

# создаем модель, объекты которой будут храниться в бд
class Vacancies(Base):
    __tablename__ = "vacancies"

    index = Column(Integer, primary_key=True, index=True)
    custom_position = Column(String)
    experience = Column(Integer)
    salary = Column(Integer)
    city_name = Column(String)


class Resumes(Base):
    __tablename__ = "resumes"

    index = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    salary = Column(Integer)
    vacancy = Column(String)
    education = Column(String)
    city_name = Column(String)