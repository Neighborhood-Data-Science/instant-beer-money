FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY main_lambda.py ./

CMD ["main_lambda.lambda_handler"]