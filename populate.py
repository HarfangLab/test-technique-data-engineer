"""
    Script to launch the population of the datawarehouse with random data
"""

from database import load

from pathlib import Path

load(Path("populate/"))
