import boto3
import json
from data_fetch import getInfo, getHistoricalData, writeFinancialReport, getBalanceSheet, getCashFlowStatement, getIncomeStatement, convertToJson

def create_client():
    s3 = boto3.client("s3")
    return s3

def get_tech_company_data_bucket():
    s3 = create_client()
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        if bucket["Name"] == "tech-company-data":
            print("Bucket already exists", bucket["Name"])

def populate_bucket_info(ticker_name, bucket_name = "tech-company-data"):
    s3 = create_client()
    key = f"info/{ticker_name}.json"
    s3.put_object(Bucket=bucket_name, Key=key, Body=getInfo(ticker_name).encode("utf-8"))
    
def populate_bucket_historical_data(ticker_name, bucket_name = "tech-company-data"):
    s3 = create_client()
    key = f"historical-data/{ticker_name}.json"
    s3.put_object(Bucket=bucket_name, Key=key, Body=getHistoricalData(ticker_name, period='5y', interval='1d').to_json().encode("utf-8"))

def populate_bucket_financial_data(ticker_name, bucket_name = "tech-company-data"):
    s3 = create_client()
    key = f"financial-data/{ticker_name}.json"
    s3.put_object(Bucket=bucket_name, Key=key, Body=convertToJson(writeFinancialReport(ticker_name)).encode("utf-8"))

"""with open("../data/tech_company_tickers.json", "r") as file:
    tickers = json.load(file)
    for element in tickers["tech_companies"]:
        try:
            print("trying to populate bucket with: ", element)
            populate_bucket_financial_data(element)
        except Exception as e:
            print("the symbol that failed is: ", element)
            print(e)
        #populate_bucket_financial_data(element)"""

with open("../data/inflation.json", "r") as file:
    try:
        print("trying to populate bucket with: ")
        s3 = create_client()
        s3.put_object(Bucket="tech-company-data", Key="interest/interest.json", Body=file.read().encode("utf-8"))
    except Exception as e:
        print("the symbol that failed is: ")
        print(e)

