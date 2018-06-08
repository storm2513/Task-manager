import unittest

def run_tests():
    testmodules = [
        'tests.controllers_test',
        'tests.models_test',
        'tests.storage_test'
        ]

    suite = unittest.TestSuite()

    for t in testmodules:
        suite.addTests(unittest.defaultTestLoader.loadTestsFromName(t))

    unittest.TextTestRunner().run(suite)


if(__name__ == "tests.run_tests"):
    run_tests()
