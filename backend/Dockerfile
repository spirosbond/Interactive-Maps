FROM python:3.11

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV APP_HOME=/root
WORKDIR $APP_HOME

COPY app $APP_HOME/app
# COPY tests $APP_HOME/tests
COPY .env $APP_HOME
COPY app_config.yaml $APP_HOME
# COPY Makefile $APP_HOME

# CMD ["make", "test"] 
# CMD ["pytest", "-s", "-p", "no:warnings"]
# CMD ["make", "run"] 
EXPOSE 8080
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
