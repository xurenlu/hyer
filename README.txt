= About Hyer =
    Hyer is a vertical search cralwer library written in python. It
provides a number of methods to mine data from kinds of sites.
== Features ==
  + robots.txt protocol supported;
  + by setting how many visits per minute ,you can avoid to visit site too frequencly;
  + you can setup proxies to tell target web server various IP addresses;
  + cache URL 's HTML;
  + extract MainText from HTML by specific a * link-threshold *
  + visit sites with cookie;

==About Worker==
    The Hyer Vertical Search run in mutltiThread mode and simulate a
    production line.First we define the <b>rules</b>,and we define
    <b>workers</b>. Each Worker run in a new thread.When workers finish
    their task,Then ask the leader to fetch a new task.
    A worker have a "skill";We bind each worker with a filter or a source or
    dbwriter and something else. Workers request leader to task;
== about VSR class ==
VSR是vertical search crawler的简称。它运行各个 builder,builder则运行属于它的filters.

== about Filter class ==
    Filter是定义如何对数据进行操作处理，比如替换操作，删除元素等。
    为了调试，特意加了一个DisplayFilter.这个操作打印出当前步骤的公共数据。
    一连串的filter组合在一起形成一个处理链.

== about Source class==
    Source决定了进行多少次由一组filter进行的处理链.

== about builders class ==
    Builders之间的数据是不共享的。
    每个builder开始时重新初始化全局数据，这个数据在各个filters之间传递下去。
    <line-throuth>因此，每个builder最好以一个source类的filter开始，以一下dbwriter类的filter结束
。 </line-through>
