import yaml


_config = None

def load_config():
    global _config
    if _config is None:
        with open('config.yml') as f:
            _config = yaml.load(f, Loader=yaml.FullLoader)

    return _config

def config(name=None):
    '''获取配置
    
    :param name
    name 多级查询，通过“.”相连，如：db.host

    host = config('db.host')

    '''
    if _config is None:
        load_config()

    if name is None:
        return _config
    else:
        _cfg = _config
        fields = name.split('.')
        for field in fields:
            if field in _cfg:
                _cfg = _cfg[field]
            else:
                raise KeyError('field %s not found in config file' % field)
        return _cfg