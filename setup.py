from setuptools import setup, find_packages

setup(name='ka2hyeon_allweather',
      version='0.0.1',
      description='ka2hyeon allweather portfolio automation',
      url='https://https://github.com/ka2hyeon/allweather',
      author='Park, Jhyeon',
      author_email='ka2hyeon@gmail.com',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=['numpy-stl']
)

