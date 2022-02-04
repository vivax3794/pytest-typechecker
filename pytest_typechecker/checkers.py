import subprocess
import json
import os

import pytest

class TypingCheckingError(Exception):
    """Custom exception for error reporting."""

class PyrightTypecheck(pytest.Item):
    def __init__(self, parent):
        super().__init__("pyright", parent)
        self.add_marker("typing")
        self.add_marker("pyright")

    def runtest(self):
        result = subprocess.run(["pyright", "--outputjson", str(self.fspath)], capture_output=True)
        data = json.loads(result.stdout.decode())

        amount_errors = data["summary"]["errorCount"]
        if amount_errors != 0:
            raise TypingCheckingError(self, data["generalDiagnostics"])
    
    def repr_failure(self, excinfo):
        """Called when runtest() fails"""
        if isinstance(excinfo.value, TypingCheckingError):
            errors = []
            for error in excinfo.value.args[1]:
                if error["severity"] == "error":
                    msg = error["message"]
                    type_ = error["rule"]
                    linenum = error["range"]["start"]["line"]

                    errors.append(f"line {linenum} #{type_}: {msg}")

            return "\n".join(errors)

    def reportinfo(self):
        return self.fspath, 0, f"pyright: {type(self.fspath)(os.curdir).bestrelpath(self.fspath)}"

class MypyTypecheck(pytest.Item):
    def __init__(self, parent):
        super().__init__("mypy", parent)
        self.add_marker("typing")
        self.add_marker("mypy")

    def runtest(self):
        result = subprocess.run(["mypy", str(self.fspath)], capture_output=True)
        if result.returncode != 0:
            error_msg = result.stdout.decode()
            raise TypingCheckingError(self, error_msg)
    
    def repr_failure(self, excinfo):
        """Called when runtest() fails"""
        return excinfo.value.args[1]

    def reportinfo(self):
        return self.fspath, 0, f"mypy: {type(self.fspath)(os.curdir).bestrelpath(self.fspath)}"



TYPECHECKERS = {
    "pyright": PyrightTypecheck,
    "mypy": MypyTypecheck
}