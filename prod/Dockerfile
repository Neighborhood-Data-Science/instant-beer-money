FROM umihico/aws-lambda-selenium-python:latest

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY main_lambda.py ./

CMD ["main_lambda.lambda_handler"]