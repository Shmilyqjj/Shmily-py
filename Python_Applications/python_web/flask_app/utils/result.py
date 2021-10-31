def success(data=None):
    return {'code': 20000, 'data': data, 'msg': 'success'}


def error(msg='系统异常'):
    return {'code': 50000, 'data': None, 'msg': msg}


def success_page(data, total_size, page=1, page_size=10):
    return {'code': 20000, 'msg': 'success',
            'data': {'data': data, 'totalSize': total_size, 'page': page, 'pageSize': page_size}
            }

