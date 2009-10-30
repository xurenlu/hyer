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

setup(
	name = "Hyer",
	version = "0.66",
	url = 'http://www.162cm.com/',
	author = '162cm',
	author_email = 'xurenlu@gmail.com',
	description = 'python files for WWW spider and index,search .',
	license = 'LGPL V2',
	packages = find_packages(),
	package_data ={
		'':['ANNOUNCE', 'AUTHORS', 'ChangeLog', 'INSTALL',
'LICENSE.TXT', 'README', 'TODO'],
		'hyer.tests': ['tests/*.py']
   },
)
