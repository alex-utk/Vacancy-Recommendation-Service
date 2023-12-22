from typing import Dict
from sqlalchemy.orm import Session
import nmslib
from sentence_transformers import SentenceTransformer
import pandas as pd
import os

DATA_PATH = './DATA/'


def load_encoder() -> SentenceTransformer:
    encoder = SentenceTransformer('cointegrated/rubert-tiny2')
    encoder.cuda()
    # return None
    return encoder

def load_ann_models() -> Dict[nmslib.dist.IntIndex, nmslib.dist.IntIndex]:
    vacnaсies = nmslib.init(method='hnsw', space='cosinesimil',
                            data_type=nmslib.DataType.DENSE_VECTOR)
    vacnaсies.loadIndex(os.path.join(DATA_PATH, 'vacancies/vacancy_index'), load_data=True)

    resumes = nmslib.init(method='hnsw', space='cosinesimil',
                          data_type=nmslib.DataType.DENSE_VECTOR)
    resumes.loadIndex(os.path.join(DATA_PATH, 'resumes/resume_index'), load_data=True)

    return {'vacanсies': vacnaсies,
            'resumes': resumes}


def load_dataframes() -> tuple[pd.DataFrame, pd.DataFrame]:
    data_resume = pd.read_pickle(os.path.join(DATA_PATH,
                                              'hh_resume_processed.pkl'))
    data_vacancy = pd.read_pickle(os.path.join(DATA_PATH,
                                               'hh_vacancies_processed.pkl'))

    return data_resume, data_vacancy

def get_from_db(engine, idx_list, table_class) -> list:
    with Session(autoflush=False, bind=engine) as db:
        q = db.query(table_class).filter(table_class.index.in_(list(idx_list)))
    result = q.all()

    return result
