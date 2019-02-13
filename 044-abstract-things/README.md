# 抽象对象风格

## 约束

- 较大问题被分解为问题域相关的**抽象对象**，定义对象抽象的行为
- 具体对象以某种方式与抽象对象绑定
- 应用程序其他部分**不依赖对象的内容，而依赖对象的行为**

## 注解

在抽象对象风格中，抽象操作按照名称和其接收及返回的参数定义。程序第一阶段，**不存在具体对象，只有抽象对象**，定义了访问其建模的数据结构的方法；第二阶段中，根据抽象对象给出具体实现。

示例程序运用 **Python 抽象基类（Abstract Base Class，ABC）**来定义抽象对象 —— `IDataStorage`、`IStopWordFilter`、`IWordFrequencyCounter`。

``` python
import abc

class IDataStorage (metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def words(self):
        pass

class IStopWordFilter (metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def is_stop_word(self, word):
        pass

class IWordFrequencyCounter (metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def increase_count(self, word):
        pass
    
    @abc.abstractmethod
    def sorted(self, word):
        pass
```

抽象对象的任何实现都必须提供抽象类中定义操作的具体实现。这些具体实现类也作为**实现具体数据结构的机制，通过其实现的过程访问**。类本身与已定义的 ABC 抽象基类无关联，但通过抽象基类的`register`方法实现动态联系。

``` python
class DataStorageManager:
    _data = ''
    
class StopWordManager:
    _stop_words = []
    
class WordFrequencyManager:
    _word_freqs = {}

IDataStorage.register(subclass=DataStorageManager)
IStopWordFilter.register(subclass=StopWordManager)
IWordFrequencyCounter.register(subclass=WordFrequencyManager)
```

抽象风格常同**强类型**一起使用，如 Java 和 C# 都通过**接口**概念支持抽象对象风格。在强类型语言中，抽象对象概念支持**is-a从属关系从具体代码重用分离**出来的程序设计。接口被用于**强制执行预计参数类型**，并在不适用具体实现类的情况下返回值。

Python 是动态类型语言，但可通过**装饰器**在特定方法或构造函数调用时，不改变源代码的情况下增加**运行时的类型检查**。`class AcceptTypes`装饰的函数声明调用时，其构造函数`__init__`和方法`__call__`将被自动调用：

``` python
# 定义装饰器类
class AcceptTypes():
    def __init__(self, *args):
        self._args = args
    # 包装函数调用
    def __call__(self, f):
        def wrapped_f(*args):
            for i in range(len(self._args)):
                if self._args[i] == 'primitive' and type(args[i + 1]) in (str, int, float, bool):
                    continue
                if not isinstance(args[i + 1], globals()[self._args[i]]):
                    raise TypeError("Wrong Type")
                
            f(*args)
               
        return wrapped_f


class DataStorageManager(IDataStorage):
    _data = ''
    
    @AcceptTypes('primitive', 'IStopWordFilter')
    def __init__(self, path_to_file, word_filter):
        # ...

# ...

class WordFrequencyController:
    @AcceptTypes('IDataStorage', 'IWordFrequencyCounter')
    def __init__(self, data_storage, word_freq_counter):
        self._storage = data_storage
        self._word_freq_counter = word_freq_counter
    # ...


stop_word_manager = StopWordManager()
storage = DataStorageManager(sys.argv[1], stop_word_manager)
word_freq_counter = WordFrequencyManager()
WordFrequencyController(storage, word_freq_counter).run()
```

## 发展历程

**抽象对象**风格最早出现于20世纪70年代早期，几乎与 OOP 语言处于同一时期。很多现代编程语言包含了某种形式的抽象对象概念。Java 和 C# 中的抽象对象是接口，可以在类型上参数化；Haskell 作为强类型纯函数语言，其抽象对象概念表现为类型类；C++ 拥有抽象类。

大型系统设计中，往往针对第三方组件的抽象定义，而非具体实现进行设计。抽象接口的实现根据涉及的编程语言而定。