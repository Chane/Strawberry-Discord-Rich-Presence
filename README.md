# Strawberry Discord Rich Presence

This script reads currently playing track metadata from Strawberry (via MPRIS/DBus),
queries Discogs for release art, and updates your Discord Rich Presence.

## Requirements

- Linux desktop session with DBus
- Strawberry Music Player
- Python 3.10+

## Setup (with venv)

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. Configure credentials:

- `config.py` contains safe defaults and is tracked.
- `config_local.py` is for local secrets and is gitignored.

Edit `config_local.py` and set:

```python
APPLICATION_ID = "your_discord_application_id"
DISCOG_USER_TOKEN = "your_discogs_user_token"
```

`APPLICATION_ID` comes from your Discord developer application.
`DISCOG_USER_TOKEN` comes from your Discogs account API settings.

## Run

```bash
python3 presenceUpdater.py
```

Optional logging flags:

```bash
python3 presenceUpdater.py --verbose
python3 presenceUpdater.py --debug
```

## Testing

```bash
pytest
```

## CI

GitHub Actions workflow at `.github/workflows/build.yml` runs:

- dependency install in a venv
- flake8 lint checks
- pytest