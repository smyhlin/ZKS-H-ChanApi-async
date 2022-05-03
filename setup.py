import pathlib
import re
import sys

from setuptools import setup, find_packages

WORK_DIR = pathlib.Path(__file__).parent

# Check python version
MINIMAL_PY_VERSION = (3, 7)
if sys.version_info < MINIMAL_PY_VERSION:
    raise RuntimeError('HentaiChanApi works only with Python {}+'.format('.'.join(map(str, MINIMAL_PY_VERSION))))


def get_description():
    """
    Read full description from 'README.md'
    :return: description
    :rtype: str
    """
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    """
    Read version
    :return: str
    """
    txt = (WORK_DIR / 'hentai_chan_api_async' / '__init__.py').read_text('utf-8')
    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='hentai_chan_api_async',
    version=get_version(),
    packages=find_packages(),
    install_requires=["aiohttp>=3.7.4", "beautifulsoup4>=4.10.0", "aiograph>=0.2", "attrs==19.1.0"],
    url='https://github.com/JKearnsl/HentaiChanApi-async',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
    ],
    author='JKearnsl',
    author_email='pooolg@hotmail.com',
    description='Asynchronous wrapper over https://hentaichan.live',
    long_description=get_description(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
