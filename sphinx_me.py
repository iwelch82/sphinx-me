
from __future__ import with_statement
from datetime import datetime
from os.path import abspath, dirname, join, isdir, splitext
from os import listdir, sep
import sys


def install():
    """
    Main entry point for running sphinx_me as a script.
    Creates a docs directory in the current directory and adds the
    required files for generating Sphinx docs from the project's
    README file - a conf module that calls setup_conf() from this
    module, and an index file that includes the project's README.
    """
    pass

def get_version(module):
    """
    Attempts to read a version attribute from the given module that
    could be specified via several different names and formats.
    """
    version_names = ["__version__", "get_version", "version"]
    version_names.extend([name.upper() for name in version_names])
    for name in version_names:
        try:
            version = getattr(module, name)
        except AttributeError:
            continue
        if callable(version):
            version = version()
        try:
            version = ".".join([unicode(i) for i in version.__iter__()])
        except AttributeError:
            pass
        return version

def setup_conf(conf_globals):
    """
    Setup function that is called from within the project's
    docs/conf.py module that takes the conf module's globals() and
    assigns the values that can be automatically determined from the
    current project, such as project name, package name, version and
    author.
    """
    project_path = abspath(join(dirname(conf_globals["__file__"]), ".."))
    sys.path.insert(0, project_path)
    authors_file = "AUTHORS"
    version = None
    author = None
    ignore = ("setup.py",)

    # Iterate through each of the files in the project's directory,
    # looking for an AUTHORS file for the project's author, or
    # importable packages/modules for the version.
    for name in listdir(project_path):
        path = join(project_path, name)
        if name.upper() == authors_file:
            with open(path, "r") as f:
                for line in f.readlines():
                    line = line.strip("*- \n\r\t")
                    if line:
                        author = line
                        break
        elif name not in ignore and (isdir(path) or splitext(name)[1] == ".py"):
            try:
                module = __import__(name)
            except (ImportError, ValueError):
                continue
            version = get_version(module)
            if version is not None:
                try:
                    author = getattr(module, "__author__")
                except AttributeError:
                    pass

    # Ask for any values that couldn't be found.
    if version is None:
        version = raw_input("No version number found, please enter one: ")
    if author is None:
        author = raw_input("No author found, please enter one: ")
        with open(join(project_path, authors_file), "w") as f:
            f.write(author)

    # Inject the minimum required names into the conf module.
    conf_globals.update({
        "version": version,
        "release": version,
        "project": project_path.rstrip(sep).split(sep)[-1],
        "master_doc": "index",
        "copyright": u"%s, %s" % (datetime.now().year, author),
    })

if __name__ == "__main__":
    install()
