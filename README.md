
# file_way	删除文件方式：
# 1：按日期
# 2：按剩余磁盘空间
# 
# over_days	设置多少天，即超过这个时间的文件将被删除
# retain_disk	设置硬盘保留空间，如果磁盘空间低于这个设置，将删除最早的文件
# path	定义需要删除的文件目录

[set]
file_way = 2
over_days = 100
retain_disk = 30
path = /Users/test
