
file_way		删除文件方式
 
file_way = 1 	按天数
file_way = 2 	按剩余磁盘空间

over_days		设置多少天，即超过这个时间的文件将被删除。
retain_disk		设置硬盘保留空间，如果磁盘空间低于这个设置，将删除最早的文件。
path			定义需要删除的文件路径

config.cfg 		配置文件改为.cfg格式，ini格式，windows下用记事本编辑会加入乱码，造成读取配置文件错误。

[set]
file_way = 2
over_days = 100
retain_disk = 30
path = /Users/test
