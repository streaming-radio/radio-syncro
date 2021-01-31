from setuptools import setup

setup(name="syncro-backend",
      version="0.0.1",
      description="Syncro des radios pour spotify",
      author="Mickael VINET",
      author_email="mail@mvinet.fr",
      packages=["syncro"],
      install_requires=["requests", "bs4"])
