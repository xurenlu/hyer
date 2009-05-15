
关于Filter:
    Filter是定义如何对数据进行操作处理，比如替换操作，删除元素等。
    为了调试，特意加了一个DisplayFilter.这个操作打印出当前步骤的公共数据。
    一连串的filter组合在一起形成一个处理链.
关于Source:
    Source决定了进行多少次由一组filter进行的处理链.
关于builders:
    Builders之间的数据是不共享的。
    每个builder开始时重新初始化全局数据，这个数据在各个filters之间传递下去。
    <line-throuth>因此，每个builder最好以一个source类的filter开始，以一下dbwriter类的filter结束
。 </line-through>
VSR是vertical search crawler的简称。它运行各个
builder,builder则运行属于它的filters.
