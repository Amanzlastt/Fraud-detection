FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --ni-cache-dir -r /code/requirements.txt
COPY ./app /code/app
EXPOSE 500
CMD ["python", "serve_model.py"]

 