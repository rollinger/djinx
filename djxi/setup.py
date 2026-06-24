from setuptools import setup

if __name__ == "__main__":
    # setup.cfg holds metadata and options. This minimal wrapper ensures
    # setuptools will read setup.cfg when building wheels/sdist.
    #
    # Add custom build logic here later if needed (preprocessing, dynamic
    # versioning, etc.) before calling setup().
    setup()
