# MyCtfTools
### 简介
本工具用来通过pyc被show_file.py解析后的文本来还原pyc文件，前提是各项元素不可缺少
原理是pyc各个属性具有一定存放顺序，pycdump出来以后没有丢失数据，仅仅是做了可视化处理，因此可以逆向还原出pyc的binary
### 说明
目前有两种show_file.py，都放在目录下了，可以尝试对pyc文件进行处理来比对
区别大概有两点
1. 属性标题一种为`argcount`另一种为`<argcount>xxx</argcount>`
2. 排列顺序一种将consts放在names之前，另一种将consts放在之后

我写的脚本仅能针对前者，而本题遇到的后者需要手动修改一下
不过替换难度也不大，通过正则替换还是比较容易的

[具体原理](https://blog.csdn.net/whklhhhh/article/details/80842694)
### 使用方法
pyc_construct.py opcode.txt > code.pyc

### 题目
SUCTF Python大法好
网鼎杯第三场 最好的语言
