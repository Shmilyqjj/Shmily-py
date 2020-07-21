#!/usr/bin/env python
# encoding: utf-8
"""
:Description: 利用cython将py编译成so
:Author: Arvin  佳境Shmily
:Create Time: 2020/7/21 22:54
:File: py2so
:Site: shmily-qjj.top
执行前提：
    系统安装python-devel 和 gcc
    Python安装cython
编译某个文件夹：
    python py2so.py mydir_path
生成结果：
    mydir_path/build文件夹下即为结果目录
生成完成后：
    在 mydir_path/build/xxx 下使用ipython进入命令行，引用包即可
    启动文件还需要py/pyc担当，须将启动的py/pyc拷贝到编译目录并删除so文件
    如项目包含如main.py的启动文件，可将源文件copy至 build/下对应位置启动
"""
import sys, os, shutil, time
from distutils.core import setup
from Cython.Build import cythonize

starttime = time.time()
setupfile= os.path.join(os.path.abspath('.'), __file__)


def getpy(basepath=os.path.abspath('.'), parentpath='', name='', build_dir="build",
          excepts=(), copyOther=False, delC=False):
    """
    获取py文件的路径
    :param basepath: 根路径
    :param parentpath: 父路径
    :param name: 文件/夹
    :param excepts: 排除文件
    :param copy: 是否copy其他文件
    :return: py文件的迭代器
    """
    fullpath = os.path.join(basepath, parentpath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
        if os.path.isdir(ffile) and ffile != os.path.join(basepath, build_dir) and not fname.startswith('.'):
            for f in getpy(basepath, os.path.join(parentpath, name), fname, build_dir, excepts, copyOther, delC):
                yield f
        elif os.path.isfile(ffile):
            # print("\t", basepath, parentpath, name, ffile)
            ext = os.path.splitext(fname)[1]
            if ext == ".c":
                if delC and os.stat(ffile).st_mtime > starttime:
                    os.remove(ffile)
            elif ffile not in excepts and ext not in('.pyc', '.pyx'):
                # print("\t\t", basepath, parentpath, name, ffile)
                if ext in('.py', '.pyx') and not fname.startswith('__'):
                    yield os.path.join(parentpath, name, fname)
                elif copyOther:
                        dstdir = os.path.join(basepath, build_dir, parentpath, name)
                        if not os.path.isdir(dstdir): os.makedirs(dstdir)
                        shutil.copyfile(ffile, os.path.join(dstdir, fname))
        else:
            pass

if __name__ == "__main__":
    currdir = os.path.abspath('.')
    parentpath = sys.argv[1] if len(sys.argv)>1 else "."

    currdir, parentpath = os.path.split(currdir if parentpath == "." else os.path.abspath(parentpath))
    build_dir = os.path.join(parentpath, "build")
    build_tmp_dir = os.path.join(build_dir, "temp")
    print("start:", currdir, parentpath, build_dir)
    os.chdir(currdir)
    try:
        #获取py列表
        module_list = list(getpy(basepath=currdir,parentpath=parentpath, build_dir=build_dir, excepts=(setupfile)))
        print(module_list)
        setup(ext_modules = cythonize(module_list),script_args=["build_ext", "-b", build_dir, "-t", build_tmp_dir])
        module_list = list(getpy(basepath=currdir, parentpath=parentpath, build_dir=build_dir, excepts=(setupfile), copyOther=True))
    except Exception as ex:
        print("error! ", ex)
    finally:
        print("cleaning...")
        module_list = list(getpy(basepath=currdir, parentpath=parentpath, build_dir=build_dir, excepts=(setupfile), delC=True))
        if os.path.exists(build_tmp_dir): shutil.rmtree(build_tmp_dir)

    print("complate! time:", time.time()-starttime, 's')