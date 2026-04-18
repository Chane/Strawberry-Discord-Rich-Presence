import ast
from pathlib import Path


def test_presence_updater_has_main_function_and_main_block():
    source = Path("presenceUpdater.py").read_text(encoding="utf-8")
    tree = ast.parse(source)

    function_names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "main" in function_names

    has_main_guard = False
    for node in tree.body:
        if isinstance(node, ast.If):
            test = node.test
            if (
                isinstance(test, ast.Compare)
                and isinstance(test.left, ast.Name)
                and test.left.id == "__name__"
                and len(test.ops) == 1
                and isinstance(test.ops[0], ast.Eq)
                and len(test.comparators) == 1
                and isinstance(test.comparators[0], ast.Constant)
                and test.comparators[0].value == "__main__"
            ):
                has_main_guard = True
                break

    assert has_main_guard
