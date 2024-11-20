from distutils.core import setup
setup(
   name='book-stats',
   version='1.0',
   packages=['beautifulsoup4','markdown','mplcyberpunk','matplotlib','wordcloud','setuptools','filedialpy','TkAgg'],
   license='GNU',
   packages=['bookstats'],
   long_description=open('README.txt').read(),
   include_package_data=True,
)
