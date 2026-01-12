class ExamplePlugin:
    """
    An example plugin demonstrating the modular architecture.
    """
    def __init__(self):
        self.name = "Hello World Plugin"

    def execute(self):
        print("Hello from the plugin system!")
