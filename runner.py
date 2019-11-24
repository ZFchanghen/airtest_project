from time import sleep

from airtest.cli.runner import AirtestCase, run_script
from argparse import *
import airtest.report.report as report
import jinja2
import shutil
import os
import io
from multiprocessing import Process
from airtest.core.android.adb import ADB


class CustomAirtestCase(AirtestCase):
    # @classmethod
    # def setUpClass(cls):
    #     super(CustomAirtestCase,cls).setUpClass()

    # def setUp(self):
    #     print("custom setup")
    #     # add var/function/class/.. to globals
    #     # self.scope["hunter"] = "i am hunter"
    #     # self.scope["add"] = lambda x: x+1
    #
    #     # exec setup script
    #     # self.exec_other_script("setup.owl")
    #     super(CustomAirtestCase, self).setUp()
    #
    # def tearDown(self):
    #     print("custom tearDown")
    #     # exec teardown script
    #     # self.exec_other_script("teardown.owl")
    #     super(CustomAirtestCase, self).setUp()

    def run_air(self, root_dir='', device=''):
        # 聚合结果
        results = []
        # 获取所有用例集
        root_log = root_dir + '\\' + 'log'
        if os.path.isdir(root_log):
            shutil.rmtree(root_log)
        else:
            os.makedirs(root_log)
            print(str(root_log) + 'is created')

        for f in os.listdir(root_dir):
            if f.endswith(".air"):
                # f为.air案例名称：手机银行.air
                airName = f
                script = os.path.join(root_dir, f)
                # airName_path为.air的全路径：D:\tools\airtestCase\案例集\log\手机银行
                print(script)
                # 日志存放路径和名称：D:\tools\airtestCase\案例集\log\手机银行1
                log = os.path.join(root_dir, 'log' + '\\' + airName.replace('.air', ''))
                print(log)
                if os.path.isdir(log):
                    shutil.rmtree(log)
                else:
                    os.makedirs(log)
                    print(str(log) + 'is created')
                output_file = log + '\\' + 'log.html'
                # global args
                args = Namespace(device=device, log=log, recording=None, script=script)
                try:
                    run_script(args, AirtestCase)
                except:
                    pass
                finally:
                    rpt = report.LogToHtml(script, log)
                    rpt.report("log_template.html", output_file=output_file)
                    result = {}
                    result["name"] = airName.replace('.air', '')
                    result["result"] = rpt.test_result
                    results.append(result)
        total_case = len(results)
        pass_case = len([i for i in results if i["result"] == 'success'])
        fail_case = len([i for i in results if i["result"] == 'fail'])
        pass_rate = '%.1f' % (pass_case / total_case * 100)
        # 生成聚合报告
        env = jinja2.Environment(
            # loader=jinja2.FileSystemLoader(root_dir),
            loader=jinja2.FileSystemLoader(os.path.dirname(os.path.realpath(__file__))),
            extensions=(),
            autoescape=True
        )
        # template =
        # env.get_template("summary_template.html", root_dir)
        print("1111" + os.getcwd())
        template = env.get_template("summary_template.html")

        html = template.render({"results": results, 'total_case': total_case, 'pass_case': pass_case,
                                'fail_case': fail_case, 'pass_rate': pass_rate})
        output_file = os.path.join(root_dir, "summary_{}.html".format(device[11:]))
        with io.open(output_file, 'w', encoding="utf-8") as f:
            f.write(html)
        print(output_file)

    def creat_pool(self, root_dir):
        # 创建并发执行
        pool = []
        devices = self.get_devices()
        if devices:
            for device in devices:
                p = Process(target=self.run_air, args=(root_dir, device))
                p.start()
                pool.append(p)
                sleep(2)
            for p in pool:
                p.join()
        else:
            print('请连接设备后再重试！')

    def get_devices(self):
        device = []
        devices = ADB().devices()
        for i in devices:
            device.append('android:///' + i[0])
        return device


if __name__ == '__main__':
    test = CustomAirtestCase()
    root = os.path.abspath(".")
    root_path = os.path.join(root, "air_case")
    print(root_path)
    device = ['android:///']
    print(test.get_devices())  # 测试设备
    # test.run_air(root_path)#执行项目
    # python runner.py E:\airtest_project-master\air_case     #脚本执行方法
    # python report.py E:\airtest_project-master\air_case\log
