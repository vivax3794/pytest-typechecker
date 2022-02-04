import pytest

from . import checkers

def pytest_configure(config):
    config.addinivalue_line("markers", "pyright: tests ran via pyright")
    config.addinivalue_line("markers", "mypy: tests ran via mypy")
    config.addinivalue_line("markers", "typing: tests ran via a type checker")


def pytest_collect_file(parent, path):
    if path.basename.startswith("test") and (
        path.basename.endswith("types.py")
        or path.basename.endswith("types_xfail.py")
    ):
        collector = TypeTestFile.from_parent(parent, fspath=path)

        if path.basename.endswith("types_xfail.py"):
            collector.add_marker("xfail")

        return collector



class TypeTestFile(pytest.File):
    def collect(self):
        filename = self.fspath.basename.split("_")

        selected_checkers = [
            checkers.TYPECHECKERS[word]
            for word in filename
            if word in checkers.TYPECHECKERS
        ]

        if not selected_checkers:
            selected_checkers = list(checkers.TYPECHECKERS.values())
        
        for word in filename:
            if word[0] == "n" and word[1:] in checkers.TYPECHECKERS:
                selected_checkers.remove(checkers.TYPECHECKERS[word[1:]])

        xfail_cheackers = [
            checkers.TYPECHECKERS[word[1:]]
            for word in filename
            if word[0] == "x" and word[1:] in checkers.TYPECHECKERS
        ]

        for item in selected_checkers:
            if item not in xfail_cheackers:
                yield item.from_parent(self)
        for item in xfail_cheackers:
            instance = item.from_parent(self)
            instance.add_marker("xfail")
            yield instance