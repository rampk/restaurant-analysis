from setuptools import setup, find_packages

setup(
    name='restaurant_analysis',
    version='0.0.2',
    description='Sentiment analysis on restaurant review',
    url='https://github.com/rampk/restaurant-analysis',
    author='Ramprakash Pavithrakannan',
    license='public',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['bin/*']},
)
