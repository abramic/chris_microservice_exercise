import unittest

model_one = {
  "prop_one": "str",
  "prop_two": "float",
  "prop_three": "bool",
  "prop_four": "int",
  "prop_five": "dict",
  "prop_six:": "list"
}

class IntrospectAgainstModel(unittest.TestCase):
    # These have to be a mutable type so that the respective test functions can mutate them as need be
    def introspect_against_model(body, model):
        
