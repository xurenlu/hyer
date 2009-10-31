Hyer 介绍 
    [项目主页 http://github.com/xurenlu/hyer/]
    Last Updated: %%date(%Y-%m-%d)



%! target:html
%! encoding: UTF-8
%! options: --toc
%! postproc(html): @@ <BR>
%! postproc(xhtml): @@ <BR>
%! postproc(html): {{(.*?)}} <\1>
%!postproc(html): {{ <
%!postproc(html): }} >

== About Hyer ==
    Hyer is a vertical search cralwer library written in python. It
provides a number of methods to mine data from kinds of sites.

== Features ==
  + robots.txt protocol supported;
  + by setting how many visits per minute ,you can avoid to visit site too frequencly;
  + you can setup proxies to tell target web server various IP addresses;
  + cache URL 's HTML;
  + extract MainText from HTML by specific a * link-threshold *
  + visit sites with cookie;


== 关于worker类 ==
    worker是完成指定的一系列操作,达到某个效果的一个过程。每个worker都有一个叫做"职位"的属性,我用post来表示了.在实际运行中每一类worker可能会有很多个在同时运行;


== 特性 ==

    + 支持robots.txt
    + 可以在抓取过程中设置每分钟访问该站点多少次
    + 可以设置代理
    + 可以根据链接的密度获得正文
    + 带cookie访问站点



