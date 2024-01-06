from projet import create_app


""" 
This piece of code specify wich of our class is the main project class.
More information on https://docs.python.org/3/library/__main__.html
"""
if __name__ == "__main__":
    create_app().run()