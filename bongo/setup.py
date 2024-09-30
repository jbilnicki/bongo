from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = "Bongo Offers Neuroscientific Graphs and Outputs"

setup(
        name='bongo'
        version=VERSION
        author='Jakub Bilnicki'
        author_email='""
        description=DESCRIPTION
        long_description=" "
        packages=find_packages()
        install_requires=['numpy', 'pandas', 'matplotlib', 'seaborn', 'opencv-python','scipy']
        
        keywords=['python', 'voltammertry', 'neuroanatomy']
        classifiers=["Intended Audience :: Researchers", "Intended Audience :: Students"]
        
     )