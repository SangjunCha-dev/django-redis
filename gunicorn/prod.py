
# bind = '0.0.0.0:8000'

# gunicorn 실행 명령 중 시스템 CPU 갯수로 workers 자동 설정
# import multiprocessing
# workers = multiprocessing.cpu_count() * 2

workers = 2
timeout = 90
max_requests = 2000
max_requests_jitter = 50
accesslog = '-'
