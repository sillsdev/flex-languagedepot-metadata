echo "Running test..."
echo "NOTE: This script must be run from the project root directory."
echo
echo

export PYTHONPATH="src:tests"

python3 -m unittest tests/test_grepEntries.py
