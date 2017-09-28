from setuptools import setup, find_packages

setup(name='hypothesis-cfg',
      version='0.2',
      description='Implementation of Hypothesis Context Free Grammar Strategy',
      url='https://github.com/mvcisback/hypothesis-cfg/',
      author='Marcell Vazquez-Chanlatte',
      author_email='marcell.vc@eecs.berkeley.edu',
      license='MIT',
      install_requires=[
          'funcy',
          'hypothesis'
      ],
      packages=find_packages(),
)
