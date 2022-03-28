from distutils.core import setup
import setuptools

setup(
    name='input-bridge',
    version='0.1.0',
    url='',
    author='Luke Zulauf',
    author_email='lzulauf@gmail.com',
    description='Tools for bridging various input devices',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'input-bridge=input_bridge.scripts.input_bridge:main',
        ]
    },
    install_requires=[
        'keyboard',
        'osascript',
        'pygame',
        'ruamel.yaml',
        'runcmd',  # required by osascript
    ]
)
