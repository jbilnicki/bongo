from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = "Bongo Offers Neuroscientific Graphs and Outputs"

setup(
        name='bongo',
        version=VERSION,
        author='Jakub Bilnicki',
        author_email="",
        url='https://github.com/jbilnicki/bongo.git',
        description=DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        package_data={'bongo': ['bongo/img/*'],},
        install_requires=[
        'numpy', 'pandas', 'matplotlib', 'seaborn', 'opencv-python','scipy'
        ],
        
        keywords=['python', 'voltammertry', 'neuroanatomy'],
        classifiers=[
        "Intended Audience :: Researchers",
        "Intended Audience :: Students",
        "Programming Language :: Python :: 3",
        "License :: GPU License",
        "Operating System :: OS Independent"
        ]
        
     )