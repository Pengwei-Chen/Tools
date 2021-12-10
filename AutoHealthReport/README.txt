之前一直很想给我写的健康打卡脚本补充一个README
正好学校健康打卡网站更新了，重新过了一遍，所以就写了一份，希望能帮助到大家
脚本可以实现自动打卡，不需要人为操作，不会跳出窗口
但是只是每天打卡选好的选项，求辅导员放过
全程大约需要10分钟

1. 安装Python Selenium库
打开cmd，执行pip install selenium

2. 抄代码
https://github.com/Pengwei-Chen/Tools/tree/main/AutoHealthReport
（翻墙）
输入学号和密码
并检查选项
我选的是有意向接种、适宜接种、*未接种*、在校、无入境情况
例如你已接种第一针，就把当前接种情况对应的"jzxgymqk"从option[3]中移动到option[1]中

3. 生成无窗口的可执行文件
打开cmd，执行pip install pyinstaller
cd到脚本所在的目录
pyinstaller -F -w "AutoHealthReport - User Version.py"
复制生成的dist文件夹中的exe，保存到一个能长期保存的路径

4. 挂载到win 10自带Task Scheduler
菜单键Task Scheduler（或者任务计划程序），右边Create Basic Task
时间设置为When I log on， Program选中之前生成的exe

参考资料：
1. https://zhuanlan.zhihu.com/p/127156300
2. https://zhuanlan.zhihu.com/p/346461019