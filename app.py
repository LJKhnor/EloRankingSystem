# pylint: disable=missing-function-docstring, unused-argument, too-many-arguments
from projet import create_app

"""This piece of code specify which of our class is the main project class.More information on 
https://docs.python.org/3/library/__main__.html"""
if __name__ == "__main__":
    # main()
    create_app().run()
