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

```ini
gunicorn "run:create_app()"
```
