# Copyright

"igor: interface for reading binary IGOR files."

from distutils.core import setup
import os.path

from igor import __version__


package_name = 'igor'
_this_dir = os.path.dirname(__file__)

setup(name=package_name,
      version=__version__,
      maintainer='W. Trevor King',
      maintainer_email='wking@tremily.us',
      url='http://blog.tremily.us/posts/%s/'.format(package_name),
      download_url='http://git.tremily.us/?p={}.git;a=snapshot;h=v{};sf=tgz'.format(package_name, __version__),
      license='GNU General Public License (GPL)',
      platforms=['all'],
      description=__doc__,
      long_description=open(os.path.join(_this_dir, 'README'), 'r').read(),
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      packages=[
        'igor',
        ],
      scripts=[
        'bin/igorbinarywave.py',
        ],
      provides=['igor (%s)' % __version__],
      )
