# 调试python代码
from scrapy.cmdline import execute

import sys
import os


# 添加执行路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])