FROM python:3.14-slim

# Create a virtualenv inside the container
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Install Django
RUN pip install "django<6"

# Copy source code
COPY src /src
WORKDIR /src
 

# REQUIRED: Bind to 0.0.0.0 so the host can access it
CMD ["python", "manage.py", "runserver", "0.0.0.0:8888"]
