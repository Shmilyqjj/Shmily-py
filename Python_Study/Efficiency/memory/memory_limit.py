import resource
import time
import psutil

# Linux系统生效 mac和win可能不生效

def limit_memory(maxsize):
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (maxsize, hard))


if __name__ == '__main__':
    p = psutil.Process()
    print(f"当前进程PID: {p.pid}")

    limit_memory(1024 * 1024 * 256)  # 限制512M ，可申请内存
    lst = []
    while True:
        lst.append("q" * 1000000)
        time.sleep(0.1)





