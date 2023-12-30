import os
import json
import sys
from pathlib import Path

import settings

import decompme_backend_path
from coreapp import compilers
from coreapp.diff_wrapper import DiffWrapper
import diff as asm_differ

def verify_test_sample(test_json_path, tool_a, tool_b):    
    with open(test_json_path) as f:
        test = json.load(f)
    
    a_obj_path = Path(os.path.join(test_json_path.parent, test_json_path.stem + "_" + tool_a + ".o"))
    b_obj_path = Path(os.path.join(test_json_path.parent, test_json_path.stem + "_" + tool_b + ".o"))

    if a_obj_path.exists() and not b_obj_path.exists():
        raise AssertionError(f"{tool_a} could compile {test_json_path}, but {tool_b} could not!")

    if not a_obj_path.exists() and b_obj_path.exists():
        raise AssertionError(f"{tool_b} could compile {test_json_path}, but {tool_a} could not!")

    if not a_obj_path.exists() and not b_obj_path.exists():
        # Neither tool could compile this sample.
        # That's okay! We just have nothing left to do.
        return

    # Both tools could compile this file.
    # Do both sets of instructions produced match?
    with open(a_obj_path, "rb") as f:
        a_obj = f.read()

    with open(b_obj_path, "rb") as f:
        b_obj = f.read()

    compiler = compilers.from_id(test["compiler"])
    platform = compiler.platform

    config = DiffWrapper.create_config(asm_differ.get_arch(platform.arch), test["diff_flags"])
    left = DiffWrapper.get_dump(a_obj, platform, test["diff_label"], config, test["diff_flags"])
    right = DiffWrapper.get_dump(b_obj, platform, test["diff_label"], config, test["diff_flags"])
    
    display = asm_differ.Display(left, right, config)
    diff_out = json.loads(display.run_diff()[0])
    
    if diff_out["current_score"] != 0:
        raise AssertionError(f"Differing assembly produced on {test_json_path} by {tool_a} and {tool_b}")

    # If we're here: everything's a-okay :)

def compare_compilations(tool_a, tool_b):
    for test_path in Path(settings.TEST_DIR).rglob("*.json"):
        if test_path.is_file():
            verify_test_sample(test_path, tool_a, tool_b)

if __name__ == "__main__":
    tool_a = sys.argv[1] if len(sys.argv) > 2 else "wine"
    tool_b = sys.argv[2] if len(sys.argv) > 2 else "wibo"

    compare_compilations(tool_a, tool_b)