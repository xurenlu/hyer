from distutils.core import setup
import os

def find_packages(where='.'):
	out = []
	stack=[('.', '')]
	while stack:
		where,prefix = stack.pop(0)
		for name in os.listdir(where):
			fn = os.path.join(where,name)
			if (os.path.isdir(fn) and
				os.path.isfile(os.path.join(fn,'__init__.py'))
			):
				out.append(prefix+name); stack.append((fn,prefix+name+'.'))
	return out

print find_packages()
setup(
	name = "Hyer",
	version = "0.6.11",
    fullname="Hyer- high performance spider ",
	author = '162cm',
	author_email = 'renlu.xu@gmail.com',
    maintainer="162cm",
    maintainer_email="renlu.xu@gmail.com",
	url = 'http://www.162cm.com/',
	description = 'A simple vertical search engine written in python ;',
	license = 'LGPL V2',
	packages = find_packages(),
    keywords=["search","crawler","vertical search","spider","chinese segment"],
    package_data ={
        'docs':['docs/'],
        'hyer.tests': ['tests/*.py']
    },
    requires=["BeautifulSoup"]
)
