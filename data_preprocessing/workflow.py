from prefect import flow, task
from minio import Minio
from dotenv import load_dotenv
import os
import pandas as pd
from prefect.logging import get_run_logger

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler


load_dotenv()


minio_client = Minio(
    os.getenv("MINIO_URL"), 
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False  
)


@task
def get_data(filename:str):
    logger = get_run_logger()
    logger.info("Fetching data from MinIO")
    obj = minio_client.get_object(
        "bankcustomerdata", 
        filename,  
    )
    df = pd.read_csv(obj)
    logger.info("Data fetched successfully")
    return df

@task
def df_fill_age_missing(df,filltype='mean'):
    logger = get_run_logger()
    logger.info(f"Filling missing values in Age column with {filltype}")
    if filltype == 'mean':
        df['Age'] = df["Age"].fillna(df['Age'].mean())
    elif filltype == 'median':
        df['Age'] = df["Age"].fillna(df['Age'].median())
    return df


@task
def encode_categorical_features(df):
    logger = get_run_logger()
    logger.info("Encoding categorical features")
    label_encoder = LabelEncoder()
    df['Geography'] = label_encoder.fit_transform(df['Geography'])
    df['Gender'] = df['Gender'].replace({
        'Male': 1,
        'Female': 0
    })
    logger.info("Categorical features encoded successfully")
    return df


@task
def scale_numeric_feature(df):
    scaler = StandardScaler()
    columns_to_scale = ['CreditScore', 'Age', 'Tenure','Balance','NumOfProducts','EstimatedSalary']
    df[columns_to_scale] = scaler.fit_transform(df[columns_to_scale])
    return df


@task
def upload_to_minio(filename:str, bucket_name:str):
    minio_client.fput_object(
        bucket_name,
        filename,
        filename
    )
    return f"{filename} uploaded successfully to {bucket_name}"

@flow
def data_preprocessing(
    filename:str = 'Churn_Modelling.csv',
    to_fill_age_missing: str = 'mean',
    test_size: float = 0.33
    ):
    df = get_data(filename)
    df = df_fill_age_missing(df=df,filltype=to_fill_age_missing)
    df = encode_categorical_features(df)
    df = scale_numeric_feature(df)

    data = df.to_csv('processed_data.csv',index=False)
    upload_to_minio('processed_data.csv','bankcustomerdata')

    return df

