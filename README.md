# Flask 框架结构

## 环境安装

```shell
conda create -n flask python=3.8
conda activate flask
cp config.yml.sample config.yml
pip install -r requirement.txt
```

## 调试

`python run.py`

## 部署

### WEB

```ini
[program:flask]
; environment=PYTHONPATH=/data/www ;
directory = /path/to/web ; 程序的启动目录
command = /root/anaconda3/envs/flask/bin/gunicorn -c /data/www/flask/gunicorn.py "run:create_app()"  ; 启动命令
autostart = true     ; 在 supervisord 启动的时候也自动启动
startsecs = 5        ; 启动 5 秒后没有异常退出，就当作已经正常启动了
autorestart = true   ; 程序异常退出后自动重启
stopasgroup=true
killasgroup=true
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = root          ; 用哪个用户启动
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /var/log/flask.log
```

### Celery

```ini
[program:celery]
directory = /data/www/flask ; 程序的启动目录
command = /root/anaconda3/envs/flask/bin/celery -A task.celery worker -l info  ; 启动命令
autostart = true     ; 在 supervisord 启动的时候也自动启动
startsecs = 5        ; 启动 5 秒后没有异常退出，就当作已经正常启动了
autorestart = true   ; 程序异常退出后自动重启
stopasgroup=true
killasgroup=true
startretries = 3     ; 启动失败自动重试次数，默认是 3
user = root          ; 用哪个用户启动
redirect_stderr = true  ; 把 stderr 重定向到 stdout，默认 false
stdout_logfile_maxbytes = 20MB  ; stdout 日志文件大小，默认 50MB
stdout_logfile_backups = 20     ; stdout 日志文件备份数
; stdout 日志文件，需要注意当指定目录不存在时无法正常启动，所以需要手动创建目录（supervisord 会自动创建日志文件）
stdout_logfile = /var/log/celery.log
```
