import importlib.util
import sys
import types
from pathlib import Path


class _FakeDBusException(Exception):
    pass


class _FakeSessionBus:
    pass


class _FakePresence:
    def __init__(self, application_id):
        self.application_id = application_id


class _FakeDiscogsClient:
    def __init__(self, app_name, user_token):
        self.app_name = app_name
        self.user_token = user_token


def test_import_and_init_with_mocked_external_dependencies(monkeypatch):
    fake_dbus = types.ModuleType("dbus")
    fake_dbus.SessionBus = lambda: _FakeSessionBus()
    fake_dbus.Interface = lambda *args, **kwargs: object()
    fake_dbus.exceptions = types.SimpleNamespace(DBusException=_FakeDBusException)

    fake_pypresence = types.ModuleType("pypresence")
    fake_pypresence.Presence = _FakePresence
    fake_pypresence.exceptions = types.SimpleNamespace(InvalidID=Exception)

    fake_discogs_client = types.ModuleType("discogs_client")
    fake_discogs_client.Client = _FakeDiscogsClient

    monkeypatch.setitem(sys.modules, "dbus", fake_dbus)
    monkeypatch.setitem(sys.modules, "pypresence", fake_pypresence)
    monkeypatch.setitem(sys.modules, "discogs_client", fake_discogs_client)

    # PresenceUpdater.__init__ uses argparse.parse_args(), so provide a minimal argv.
    monkeypatch.setattr(sys, "argv", ["presenceUpdater.py"])

    sys.modules.pop("presenceUpdater", None)
    module_path = Path(__file__).resolve().parents[1] / "presenceUpdater.py"
    spec = importlib.util.spec_from_file_location("presenceUpdater", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["presenceUpdater"] = module
    spec.loader.exec_module(module)

    updater = module.PresenceUpdater()

    assert isinstance(updater.bus, _FakeSessionBus)
    assert isinstance(updater.client, _FakePresence)
    assert isinstance(updater.discogsClient, _FakeDiscogsClient)
    assert hasattr(module, "main")
