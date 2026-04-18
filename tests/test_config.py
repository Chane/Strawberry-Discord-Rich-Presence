import ast
from pathlib import Path


def test_config_has_local_override_import_guard():
    source = Path("config.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    has_try_import = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            import_found = any(
                isinstance(stmt, ast.ImportFrom) and stmt.module == "config_local"
                for stmt in node.body
            )
            import_error_handler = any(
                isinstance(handler.type, ast.Name)
                and handler.type.id == "ImportError"
                for handler in node.handlers
                if handler.type is not None
            )
            if import_found and import_error_handler:
                has_try_import = True
                break

    assert has_try_import


def test_config_defines_expected_settings():
    source = Path("config.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    assigned_names = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_names.add(target.id)

    assert "APPLICATION_ID" in assigned_names
    assert "DISCOG_USER_TOKEN" in assigned_names
