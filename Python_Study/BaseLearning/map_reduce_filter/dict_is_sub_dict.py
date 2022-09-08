#!/usr/bin/env python
# encoding: utf-8
"""
:Author: shmily
:Create Time: 2022/9/7 下午8:29
:@File: dict_is_sub_dict.py
:@Description: 判断字典是子集
:@Site: shmily-qjj.top
"""

a = {'lastLoginAppID': 11111, 'lastLoginCity': '1500', 'lastLoginCountry': 'CN', 'lastLoginProvince': '15', 'lastLoginTime': '2022-06-06T13:20:55+08:00', 'lastLoginTimeDirect': '2022-06-06T13:20:55+08:00', 'updateTime': '2022-06-06T13:20:55+08:00', 'userid': 11111, 'loginTypeFavorIn12Month': 0, 'loginTimes': 680, 'loginPerMonth': {'m2021-06': {'times': 1}, 'm2021-08': {'times': 83}, 'm2021-09': {'times': 115}, 'm2021-10': {'times': 72}, 'm2021-11': {'times': 115}, 'm2021-12': {'times': 5}, 'm2022-01': {'times': 29}, 'm2022-02': {'times': 28}, 'm2022-03': {'times': 40}, 'm2022-04': {'times': 33}, 'm2022-05': {'times': 29}, 'm2022-06': {'times': 4}}, 'loginTimesIn12Month': 553, 'loginPlatform': {'android': 380}, 'lastLoginTimeForAppID22045': '2022-05-25T01:29:00+08:00', 'loginPlatformFavor': 0}
b = {'lastLoginCountry': 'CN', 'lastLoginTime': '2022-06-06T13:20:55+08:00', 'lastLoginCity': '1500', 'lastLoginTimeDirect': '2022-06-06T13:20:55+08:00', 'lastLoginProvince': '15', 'lastLoginAppID': 11111, 'updateTime': '2022-06-06T13:20:55+08:00', 'userid': 11111, 'loginTypeFavorIn12Month': 0, 'loginTimes': 680, 'loginPerMonth': {'m2021-06': {'times': 1}, 'm2021-08': {'times': 83}, 'm2021-12': {'times': 5}, 'm2021-11': {'times': 115}, 'm2021-10': {'times': 72}, 'm2021-09': {'times': 115}, 'm2022-01': {'times': 29}, 'm2022-02': {'times': 28}, 'm2022-03': {'times': 40}, 'm2022-04': {'times': 33}, 'm2022-05': {'times': 29}, 'm2022-06': {'times': 4}}, 'loginTimesIn12Month': 553, 'loginPlatform': {'android': 380}, 'lastLoginTimeForAppID22045': '2022-05-25T01:29:00+08:00', 'loginPlatformFavor': 0}

if a.items() <= b.items():
    print("是子集")
else:
    print("不是子集")


def isSubDict(subDict,dictionary):
    for key in subDict.keys():
        if (not key in dictionary) or (not subDict[key] == dictionary[key]):
            return False
    return True

print(isSubDict(a,b))

# 以a为准 比较a b哪些key值不同
print({k for k in a.keys() if a.get(k) != b.get(k)})