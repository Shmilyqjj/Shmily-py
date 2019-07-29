import random

#生成ip地址
ip_slices=[132,156,124,10,29,167,143,187,30,100]
def sample_ip():
    slice = random.sample(ip_slices,4)
    return ".".join( [str(item) for item in slice] )

#生成日志
def generate_log(count=10):
    while count >=1:
        query_log = "{ip}".format(ip = sample_ip())
        print(query_log)
        count = count - 1;


if __name__ == '__main__':
    generate_log();