考虑到后续更新已超出帮助打卡的范围
将不再公开
当前版本已弃用，仅供参考


配置全程大约需要10分钟

1. 安装Python Selenium库
打开cmd，执行pip install selenium

2. 抄代码
https://github.com/Pengwei-Chen/Tools/tree/main/AutoHealthReport
（翻墙）
输入学号和密码
并检查选项
我选的是有意向接种、适宜接种、已接种、在校、无入境情况
例如你已接种第一针，就把当前接种情况对应的"jzxgymqk"从option[2]中移动到option[1]中

3. 生成无窗口的可执行文件
打开cmd，执行pip install pyinstaller
cd到脚本所在的目录
pyinstaller -F -w "AutoHealthReport.py"
复制生成的dist文件夹中的exe，保存到一个能长期保存的路径

4. 挂载到win 11自带Task Scheduler
菜单键Task Scheduler（或者任务计划程序），右边Create Basic Task
时间设置为When I log on， Program选中之前生成的exe

参考资料：
1. https://zhuanlan.zhihu.com/p/127156300
2. https://zhuanlan.zhihu.com/p/346461019
