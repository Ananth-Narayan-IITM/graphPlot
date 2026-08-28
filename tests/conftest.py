"""
Shared pytest configuration and fixtures for graphPlot.
"""

import matplotlib

# Use a non-interactive backend during automated testing.
matplotlib.use("Agg")
