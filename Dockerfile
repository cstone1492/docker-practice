# 
FROM python:3.9

ARG BACKEND_ENV=general
ENV BACKEND_ENV $BACKEND_ENV

# 
WORKDIR /code

# 
COPY ./requirements/requirements.txt /code/requirements/requirements.txt

# adding flags for corporate proxy
RUN pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org --no-cache-dir --upgrade -r ./requirements/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "80"]