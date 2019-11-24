# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 21:42
# @Author  : Crazy
# @Software: PyCharm

results=[{'name':1,'result':'success'},{'name':2,'result':'fail'},{'name':3,'result':'success'}]
pass_case=len([i for i in results if i["result"] == 'fail'])
print(pass_case)

pass_rate='%.1f' % (4/5*100)
print(pass_rate)