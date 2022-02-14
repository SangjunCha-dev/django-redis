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
- redis 접속
    ```
    (venv)> docker exec -it redis_cache /bin/sh
    /data # redis-cli -h redis_cache
    ```
- redis 등록된 키 확인 
    ```
    keys *
    ```

### 3.2. 로컬 실행

```
> cd source
> python manage.py makemigrations
> python manage.py migrate
> python manage.py runserver 127.0.0.1:8000
```

## 4. 테스트

1. 회원가입(`POST /users/register/`)하여 계정을 생성합니다.
2. 로그인(`POST //users/login/`)한뒤 반환되는 `access_token`, `refresh_token` 값을 별도로 저장합니다.
3. 각 API 오른쪽 자물쇠 버튼(🔒)이나 `Authorize` 클릭합니다.
4. Value에 `access_token` 값을 입력하고 `Authorize` → `close` 순으로 클릭합니다.
5. 사용자 인증이 완료되었고 사용자 권한이 필요한 API 테스트를 진행할 수 있습니다.