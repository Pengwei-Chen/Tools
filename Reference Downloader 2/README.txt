引文下载小工具
功能：利用Scopus数据库批量下载文献所有引文

环境配置
Windows: Chrome浏览器
Mac: Chrome浏览器、Python、 Visual Studio Code、selenium和requests
# For Mac Only:
1.	Python 3: https://www.python.org/downloads/macos/
2.	Visual Studio Code: https://code.visualstudio.com/
3.	打开Terminal，执行 "Python3 -m pip install selenium" 和 "Python3 -m pip install requests"
4.	用Visual Studio Code打开Python文件，添加信任，安装Python插件，选择Python解释器路径，点击右上角运行

使用
1.	运行Reference Downloader
2.	复制文章标题到控制台（Console），按两下回车，复制的内容有换行没有关系，但有特殊排版导致“Keyboard Interrupt”需要复制到微信等聊天软件的聊天框，再复制出来
3.	脚本会自动检查Chrome Driver更新，在Scopus数据库中查找文献（输入的文献没找到会停在这一步），获取reference list，并拼凑Sci Hub链接进行下载，没有doi的paper或书不会被下载
4.	拼凑的下载链接出现404或者未找到文献是正常现象，等一会儿就行了
5.	下载过程中可能会出现无法避免的网络波动，导致下载中断或者进度条停滞。只剩下一个页签之后，打开chrome的下载页，检查一下。Network Error点击Resume；Virus Scan Failed和Deleted说明已经下完并且重命名了
6.	Paper会被下载到Python脚本同一目录下的相应文件夹中，并默认被重命名为“年份+第一作者”，Sci Hub上没有的文献会被放在unavailable.txt里

自定义PDF文件命名
PDF File Name Config.txt中，带“#”号的行是可选命名选项，最后一行是文件名形式
例如，默认的"year"_"first_author"代表年份+第一作者，中间用“_”连接，如2021_Chen, P.
你还可以选择以文章在reference list中的顺序、标题、第一作者、第一作者的姓、年份、期刊等方式命名

P.S. 推荐一下每日健康打卡脚本 (Windows)
https://github.com/Pengwei-Chen/Tools/tree/main/AutoHealthReport
