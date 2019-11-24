# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 22:21
# @Author  : Crazy
# @Software: PyCharm

import os,sys
import jinja2
if __name__ == '__main__':
    os.system("python runner.py E:\\airtest_project-master\\air_case")
    os.system("python report.py E:\\airtest_project-master\\air_case\\log")
    # os.path.abspath(os.getcwd(),)
    # print(os.path.dirname(os.path.realpath(__file__)))
    # print("1111" + os.getcwd())
    # root_dir="E:\\airtest_project-master\\air_case"
    # env = jinja2.Environment(
    #     loader=jinja2.FileSystemLoader(os.path.dirname(root_dir)),
    #     extensions=(),
    #     autoescape=True
    # )
    # # template =
    # # env.get_template("summary_template.html", root_dir)
    # print("1111" + os.getcwd())
    # template = env.get_template("summary_template.html")