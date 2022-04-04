# 信号与槽连接

PyQt5或者PySide2中提供了两种槽连接方式，它们各有优点。  

### 1. 通过connect方式连接  

* 优点：代码和逻辑关联紧密，槽函数可以复用   
* 缺点：代码繁琐（每个信号连接都需要使用connect语句）  
* 示例:  

```python
# 定义槽函数
def pushButton_slot_fun(self, x):
    print(x)

# 定义控件
push_word = QtWidgets.QPushButton('Random word')
push_word2 = QtWidgets.QPushButton('Random word')
# 槽连接，使用lambda表达式传参
push_word.clicked.connect(lambda: pushButton_slot_fun('参数1'))  
push_word2.clicked.connect(lambda: pushButton_slot_fun('参数2'))  
```
 
### 2. 通过connectSlotsByName方式连接  
  
* 优点：代码整洁美观    
* 缺点：槽函数唯一，只能传信号自带参数 [Issue](https://github.com/se7enXF/pyside2/issues/2#issuecomment-664003084)  
* 示例: 

```python
# 定义控件
push_word = QtWidgets.QPushButton('Random word')
push_word2 = QtWidgets.QPushButton('Random word')
# 必须设置控件的名称，即ObjectName
push_word.setObjectName('push_word')
push_word2.setObjectName('push_word2')

# parent为发出槽信号的控件的parent，如是当前窗口的控件发出信号，这里填self
# 这句话必须在所有setObjectName之后才会生效
QtCore.QMetaObject.connectSlotsByName(parent)

# 使用@QtCore.Slot()修饰下面的函数，说明该函数是槽函数
@QtCore.Slot()
# 槽函数名的格式为：on_[ObjectName]_[信号]
def on_push_word_clicked():
    pass

@QtCore.Slot()
def on_push_word2_clicked():
    pass
```  

### 最后  
* 之前的代码都用【designer生成+py脚本调用】的方式，认为这种方式编程快速。
在我真正部署了大项目之后，才发现完全键入的代码才更有生命力。增删改除控件在
两步走的方式中存在很大问题，而实践中这些动作是必不可少的。
* 说明一下我的代码方式。首先写出框架和基本控件，如果哪个控件的某个熟悉怎么
设置不知道，我会打开designer然后随便放置一个去查看，然后尝试使用set等命令。
如果上述方法不通，我还会打开[Qt文档](https://doc.qt.io/qtforpython/modules.html)
去查看控件的方法，函数，信号，例子。
* 之后的代码将不再使用两步走的方案，我会提供一个快捷方便的函数来构建布局。
* 下一节([第七课](../Lesson_07.主窗口的构成/readme.md))会介绍Qt主窗口的构成。