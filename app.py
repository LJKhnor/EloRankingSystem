from projet import create_app
from testElo import main

""" 
This piece of code specify wich of our class is the main project class.
More information on https://docs.python.org/3/library/__main__.html
"""
if __name__ == "__main__":
    # main()
    create_app().run()
