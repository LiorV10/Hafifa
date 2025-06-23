FROM python:3.12.3
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache- --upgrade -r /requirements.txt
COPY ./src/ .
EXPOSE 8000
CMD ["fastapi", "run", "main.py", "--port", "8000"]
