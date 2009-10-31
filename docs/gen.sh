#!/bin/bash
#txt2tags --toc -t html DEV.rule
for c in txt2tags_source/*.txt
do
    #echo $c
    txt2tags $c
done
mv txt2tags_source/*.html ./html/
#txt2tags --toc -t html DEV.rule
