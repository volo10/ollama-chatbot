"""
Test Runner for Ollama Chatbot
Runs all test suites for v1, v2, and v3
"""

import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Run all test suites"""

    print("=" * 70)
    print("OLLAMA CHATBOT - COMPLETE TEST SUITE")
    print("=" * 70)
    print()

    # Create test loader
    loader = unittest.TestLoader()

    # Create test suite
    suite = unittest.TestSuite()

    # Add test modules
    try:
        # Import test modules
        import test_chatbot_v1
        import test_chatbot_v2
        import test_chatbot_v3

        # Add test suites
        suite.addTests(loader.loadTestsFromModule(test_chatbot_v1))
        suite.addTests(loader.loadTestsFromModule(test_chatbot_v2))
        suite.addTests(loader.loadTestsFromModule(test_chatbot_v3))

    except ImportError as e:
        print(f"Error importing test modules: {e}")
        return False

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED! ✅")
        print("All versions (v1, v2, v3) are working correctly.")
        return True
    else:
        print("\n❌ SOME TESTS FAILED ❌")
        print("Please review the failures above.")
        return False


def run_specific_version(version):
    """Run tests for a specific version"""

    print("=" * 70)
    print(f"OLLAMA CHATBOT - VERSION {version} TESTS")
    print("=" * 70)
    print()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    try:
        if version == "1":
            import test_chatbot_v1
            suite.addTests(loader.loadTestsFromModule(test_chatbot_v1))
        elif version == "2":
            import test_chatbot_v2
            suite.addTests(loader.loadTestsFromModule(test_chatbot_v2))
        elif version == "3":
            import test_chatbot_v3
            suite.addTests(loader.loadTestsFromModule(test_chatbot_v3))
        else:
            print(f"Unknown version: {version}")
            return False

    except ImportError as e:
        print(f"Error importing test module: {e}")
        return False

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    print(f"Version {version} - Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)

    return result.wasSuccessful()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run Ollama Chatbot Tests')
    parser.add_argument(
        '--version',
        choices=['1', '2', '3', 'all'],
        default='all',
        help='Which version to test (default: all)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Reduce output verbosity'
    )

    args = parser.parse_args()

    # Run tests based on arguments
    if args.version == 'all':
        success = run_all_tests()
    else:
        success = run_specific_version(args.version)

    # Exit with appropriate code
    sys.exit(0 if success else 1)
