from workflow import data_preprocessing
from pathlib import Path


if __name__ == '__main__':
        data_preprocessing.from_source(
                source=str(Path(__file__).parent),
                entrypoint="workflow.py:data_preprocessing",
                ).deploy(
                        name="data-preprocessing-customer-churn",
                        work_pool_name="DataPreprocessingWorkPool",
                        cron="0 9 * * 1-5" ,
                        parameters={
                                "filename": "Churn_Modelling.csv",
                                "to_fill_age_missing": "mean",
                                "test_size": 0.33
        })
