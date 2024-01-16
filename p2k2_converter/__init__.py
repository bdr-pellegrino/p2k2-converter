import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('p2k2_converter')

# this is the initial module of your app
# this is executed whenever some client-code is calling `import p2k2_converter` or `from p2k2_converter import ...`
# put your main classes here, eg:
class MyClass:
    def my_method(self):
        return "Hello World"


# let this be the last line of this file
logger.info("p2k2_converter loaded")
