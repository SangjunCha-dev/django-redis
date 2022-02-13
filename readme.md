# Django redis 사용하기

> redis를 사용하는 django 서버입니다.
> JWT기반의 사용자 접근제어로 계정 관리 기능이 있습니다.


---

## 1. Tech/Framework Used

- python 3.9.9
- django 4.0.2
- redis 6.2.6
- postgreSQL 14.2


---

## 2. Install

### 2.1. 가상 환경 설치

```bash
> python -m venv venv
> venv\Scripts\activate
```

### 2.2. 라이브러리 requirements 설치

```bash
pip install -r requirements-[linux or windows].txt
```

### 2.3. 라이브러리 직접 설치

```bash
(venv)> pip install django

# restframework
(venv)> pip install djangorestframework
(venv)> pip install djangorestframework-simplejwt

# swagger
(venv)> pip install drf-yasg

# PostgreDB
(venv)> pip install psycopg2

# WEB - WSGI 통신
(venv)> pip install gunicorn

# redis
(venv)> pip install django-redis
```


---

## 3. 서버 실행

### 3.1. docker-compose

- docker container 실행
    ```bash
    > docker-compose -f docker-compose.yml up -d --build
    ```
- docker container 종료
    ```bash
    > docker-compose -f docker-compose.yml down
    ```

### 3.2. 로컬 실행

```
> cd source
> python manage.py runserver 127.0.0.1:8000
```