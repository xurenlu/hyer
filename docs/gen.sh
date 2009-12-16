#!/bin/bash
#txt2tags --toc -t html DEV.rule
for c in txts/*.txt
do
    #echo $c
    txt2tags $c
done
mv txts/*.html ./html/
#txt2tags --toc -t html DEV.rule
