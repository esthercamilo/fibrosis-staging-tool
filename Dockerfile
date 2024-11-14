FROM python:3.10
WORKDIR /app

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

COPY core/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /app/media

WORKDIR /app/dashboard
RUN npm install
RUN npm run build

WORKDIR /app
RUN python manage.py collectstatic --noinput

