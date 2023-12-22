import re
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, \
                       String, MetaData
from sqlalchemy.orm import Session
from sqlalchemy.orm import DeclarativeBase

from service.db_classes import Base, Vacancies, Resumes
# строка подключения
sqlite_database = "sqlite:///vacancies_and_resumes.db"

# вакансии
data_vacancy: pd.DataFrame = pd.read_pickle('/mnt/88fdd009-dda3-49d8-9888-cfd9d9d5910a/ITMO/rabota_ru_parser/hh_data_processed.pkl')
data_vacancy['salary_from'] = data_vacancy['salary_from'].fillna(50000)
data_vacancy = data_vacancy.loc[:, ['custom_position', 'experience', 'salary_from', 'city_name']]
data_vacancy['salary_from'] = data_vacancy['salary_from'].astype(int)

mapper = dict(zip(data_vacancy['experience'].unique(), [2, 4, 0, 7]))
data_vacancy['experience'] = data_vacancy['experience'].map(mapper)
data_vacancy = data_vacancy.rename(columns={'salary_from': 'salary'})

# резюме
data_resume: pd.DataFrame = pd.read_pickle('./DATA/hh_resume_processed.pkl')
data_resume['ЗП'] = data_resume['ЗП'].apply(lambda x: int(re.sub(r"\D", "", x)))
data_resume['Город'] = data_resume['Город, переезд, командировки'].apply(lambda x: x.split(',')[0].strip())
data_resume = data_resume.drop(columns=['Опыт работы', 'Занятость', 'График',
                                        'Последнее/нынешнее место работы', 'Последняя/нынешняя должность',
                                        'Обновление резюме', 'Авто','Город, переезд, командировки'])
renamer = {
    'Пол, возраст': 'description',
    'ЗП': 'salary',
    'Ищет работу на должность:': 'vacancy',
    'Образование и ВУЗ': 'education',
    'Город': 'city_name',
}
data_resume = data_resume.rename(columns=renamer)


engine = create_engine(sqlite_database)

# #создаем базовый класс для моделей
# class Base(DeclarativeBase): pass


# # создаем модель, объекты которой будут храниться в бд
# class Vacancies(Base):
#     __tablename__ = "vacancies"

#     index = Column(Integer, primary_key=True, index=True)
#     custom_position = Column(String)
#     experience = Column(Integer)
#     salary = Column(Integer)
#     city_name = Column(String)


# class Resumes(Base):
#     __tablename__ = "resumes"

#     index = Column(Integer, primary_key=True, index=True)
#     description = Column(String)
#     salary = Column(Integer)
#     vacancy = Column(String)
#     education = Column(String)
#     city_name = Column(String)


# создаем таблицы
Base.metadata.create_all(bind=engine)

data_vacancy.to_sql('vacancies', if_exists='replace', con=engine, index=True)
data_resume.to_sql('resumes', if_exists='replace', con=engine, index=True)