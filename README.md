python-2048
===========

2048小游戏的python简单实现。

最近这款小游戏非常火，想想算法也挺简单，忍不住用python实现了一个，目前还很简陋。

暂时只有终端界面，以后考虑用一种GUI美化(wxpython,qt,kivy...还没选好)，或者flask,django的web框架，都简单

目前终端只支持按键回车操作，以后考虑直接终端捕获按键，无需按回车确认。

另外，规则也不完善，比如每次新插入的数字只有2，没有加入随机数4，以后加上。

没有用堆栈存储矩阵，只是用变量存储了一次，所以只能撤销一部，无法一直撤销，以后也容易改。
