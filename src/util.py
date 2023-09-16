def deep_get(data, key, default=None, raising=False):
    value = data
    try:
        for key in key.split('/'):
            if isinstance(value, dict):
                value = value[key]
                continue
            else:
                if raising:
                    raise KeyError
                return default
    except KeyError:
        if raising:
            raise
        return default
    else:
        return value
