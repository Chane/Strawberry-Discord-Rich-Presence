"""Project configuration defaults.

Keep safe placeholders in version control and put real local secrets in
config_local.py (which should be gitignored).
"""

APPLICATION_ID = ""
DISCOG_USER_TOKEN = ""

# ============================================================================
# Import local config overrides if they exist
# ============================================================================
try:
	from config_local import *  # noqa: F401, F403
except ImportError:
	# config_local.py doesn't exist - using defaults (expected in CI/tests)
	pass