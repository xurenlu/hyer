all:
	python amazon.py
a2ll:
	#./test.py 13*.html
	#python main.py
	rm data/ -rf
	mkdir data/rss/ -p
	python rss_digg.py
	cat data/rss/_log*
py:
	ps -Awwwf|grep python --color=auto
tar:
	tar czf hyer.tar.gz hyer/*.py setup.py main.py Changelog
