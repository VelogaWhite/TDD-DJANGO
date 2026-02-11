# Use a stable Python version
FROM python:3.12-slim

# 1. Create nonroot user
RUN adduser --uid 1234 nonroot

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY requirements.txt /tmp/requirements.txt
# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

COPY src /src
WORKDIR /src

# 2. Run collectstatic with a dummy secret key (Prevents build crashes)
RUN DJANGO_SECRET_KEY=build-only-key python manage.py collectstatic --noinput

# 3. Transfer ownership to nonroot
RUN chown -R nonroot:nonroot /src
RUN chown -R nonroot:nonroot /venv

ENV DJANGO_DEBUG_FALSE=1

# 4. Switch user
USER nonroot

# Run migration and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind :7860 superlists.wsgi:application"]
