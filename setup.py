import setuptools

import os
from io import open  # for Python 2 (identical to builtin in Python 3)

from setuptools import find_packages, setup


def pyload(name):
    ns = {}
    with open(name, encoding="utf-8") as f:
        exec(compile(f.read(), name, "exec"), ns)
    return ns


# In case it's Python 2:
try:
    execfile
except NameError:
    pass
else:
    def pyload(path):
        ns = {}
        execfile(path, ns)
        return ns


repo_root = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(repo_root, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


ns = pyload(os.path.join(repo_root,  "dpmmpython", "release.py"))
version = ns["__version__"]



setup(name='dpmmpython_trax',
      version=version,
      description="Python wrapper for DPMMSubClusters julia package",
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Or Dinari',
      author_email='dinari@post.bgu.ac.il',
      license='MIT',
      keywords='julia python',
      classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        #'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
      ],
      url='https://github.com/dinarior/dpmmpython_trax',
      project_urls={
          "Source": "https://github.com/dinarior/dpmmpython_trax",
          "Tracker": "https://github.com/dinarior/dpmmpython_trax/issues",
          "Documentation": "https://bgu-cs-vil.github.io/DPMMSubClusters.jl/latest/",
      },
      packages=find_packages(),
      install_requires=[
          'julia','wget','numpy'
      ],
      extras_require={
          # Update `ci/test-upload/tox.ini` when "test" is changed:
          "test": [
              "numpy",
              "ipython",
              # pytest 4.4 for pytest.skip in doctest:
              # https://github.com/pytest-dev/pytest/pull/4927
              "pytest>=4.4",
              "mock",
          ],
      },
      )


import julia
import sys
import wget
import tarfile
from julia.api import Julia



def get_julia_path_from_dir(base_dir):
    dir_content = os.listdir(base_dir)
    julia_path = base_dir
    for item in dir_content:
        if os.path.isdir(os.path.join(julia_path,item)):
            julia_path = os.path.join(julia_path,item)
            break

    return os.path.join(julia_path,'bin','julia'),os.path.join(julia_path,'bin')



def install(julia_download_path = 'https://julialang-s3.julialang.org/bin/linux/x64/1.5/julia-1.5.3-linux-x86_64.tar.gz', julia_target_path = None):
    '''
    :param julia_download_path: Path for the julia download, you can modify for your preferred version
    :param julia_target_path: Specify where to install Julia, if not specified will install in $HOME$/julia
    '''
    if julia_target_path == None:
        julia_target_path = os.path.join(os.path.expanduser("~"),'julia')
    if not os.path.isdir(julia_target_path):
        os.mkdir(julia_target_path)
    else:
        return    
    download_path = os.path.join(julia_target_path,'julia_install.tar.gz')
    print("Downloading Julia:")
    wget.download(julia_download_path, download_path)
    print("\nExtracting...")
    tar = tarfile.open(download_path,"r:gz")
    tar.extractall(julia_target_path)
    _, partial_path = get_julia_path_from_dir(julia_target_path)
    os.environ["PATH"] += os.pathsep + partial_path
    os.system("echo '# added by dpmmpython' >> ~/.bashrc")
    os.system("echo 'export PATH=\""+partial_path+":$PATH\"' >> ~/.bashrc")
    print("Configuring PyJulia")    
    julia.install()
    julia.Julia(compiled_modules=False)
    print("Adding DPMMSubClusters package")  
    from julia import Pkg
    Pkg.add("DPMMSubClusters")
    print("Please exit the shell and restart, before attempting to use the package") 



install()