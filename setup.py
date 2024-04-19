"""File providing setup for the project"""
from setuptools import setup

setup(name="EloRankingSystem",
      version="0.1",
      description="A python application for the Elo Rating System",
      long_description="""
      A python application for the Elo Rating System
      It provide a backend system to manage ELO league, 
      and will provide a web application to allow user to create and manage their ELO league.
      """,
      author1="Lejeune Joachim (LJKhnor)",
      author2="Rosier Gilles (Yukimushide92)",
      author1_email="",
      original_author="Hank Hang Kai Sheehan",
      original_author_email="hanksheehan@gmail.com",
      url="https://github.com/LJKhnor/EloRankingSystem.git",
      include_package_data=True,
      license="MIT",
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License"
      ]
      )
