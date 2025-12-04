FROM python:3.14
WORKDIR /app

# Install Poetry
RUN pip install poetry


# Turn-off Poetry-venv, so that the dependencies go directly to /usr/local
RUN poetry config virtualenvs.create false \
 && poetry config virtualenvs.in-project false


RUN pip install --upgrade pip setuptools wheel
RUN pip uninstall -y urllib3 || true
RUN pip install urllib3==2.4.0
# Copy the dependency manifests and install them
COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction

# Copy all code of app
COPY . .


EXPOSE 8003
CMD ["python", "manage.py", "runserver", "0.0.0.0:8003"]