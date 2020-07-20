#!/usr/bin/env python
# encoding: utf-8
"""
:Description:modin pandas test 并发 分布式pandas执行
:Author: 佳境Shmily
:Create Time: 2020/7/20 23:15
:File: modin_test
:Site: shmily-qjj.top
"""
def pandas_test():
    import pandas as pd
    from time import time
    df = pd.DataFrame(zip(range(1000000),range(1000000,2000000)),columns=['a','b'])
    start = time()
    df['c'] = df.apply(lambda x: x.a+x.b ,axis=1)
    df['d'] = df.apply(lambda x: 1 if x.a%2==0 else 0, axis=1)
    print('pandas_df.apply Time: {:5.2f}s'.format(time() - start))
    start = time()
    group_df = df[['d','a']].groupby('d',as_index=False).agg({"a":['sum','max','min','mean']})
    print('pandas_df.groupby Time: {:5.2f}s'.format(time() - start))
    # start = time()
    # data = pd.read_csv('test_modin.csv')
    # print('pandas_df.read_csv Time: {:5.2f}s'.format(time() - start))


def modin_pandas_test():
    import modin.pandas as pd
    from time import time
    df = pd.DataFrame(zip(range(1000000),range(1000000,2000000)),columns=['a','b'])
    start = time()
    df['c'] = df.apply(lambda x:x.a+x.b ,axis=1)
    df['d'] = df.apply(lambda x:1 if x.a%2==0 else 0, axis=1)
    print('modin_pandas_df.apply Time: {:5.2f}s'.format(time() - start))
    start = time()
    group_df = df[['d','a']].groupby('d',as_index=False).agg({"a":['sum','max','min','mean']})
    print('modin_pandas_df.groupby Time: {:5.2f}s'.format(time() - start))
    # start = time()
    # data = pd.read_csv('test_modin.csv')
    # print('modin_pandas_df.read_csv Time: {:5.2f}s'.format(time() - start))


if __name__ == '__main__':
    pandas_test()
    modin_pandas_test()





