import json
import os
from pathlib import Path
import sys
import multiprocess

import settings

import decompme_backend_path
from coreapp import compilers
import coreapp.compiler_wrapper
from coreapp.compiler_wrapper import CompilerWrapper
from coreapp.error import CompilationError

def compile_test_sample(test_path, emulator_tool_name):
    with open(test_path) as f:
        test = json.load(f)

    try:
        result = CompilerWrapper.compile_code(
            compilers.from_id(test["compiler"]),
            test["compiler_flags"],
            test["source_code"],
            test["context"],
            test["diff_label"],
            tuple(test["libraries"]),
        )

        # Once we have our compiled object file, persist it to disk
        # (making sure to tag the name of the tool that generated it on)
        test_obj_path = os.path.join(test_path.parent, test_path.stem + "_" + emulator_tool_name + ".o")
        with open(test_obj_path, "wb") as f:
            f.write(result.elf_object)

    except CompilationError as e:
        print (e)
        
def walk_tests(emulator_tool_path, emulator_tool_name):
    # This could definitely be cleaner, but this is currently the only way decomp.me allows for specifying the name
    # of the wibo binary externally 
    coreapp.compiler_wrapper.WIBO = emulator_tool_path

    # Grab *all* the things that need compiling ...
    test_samples = []

    for test_path in Path(settings.TEST_DIR).rglob("*.json"):
        if test_path.is_file():
            test_samples.append(test_path)

    # ... and compile them!
    with multiprocess.Pool(settings.PARALLELISATION_FACTOR) as p:
        p.map(lambda x: compile_test_sample(x, emulator_tool_name), test_samples)

if __name__ == "__main__":
    emulator_tool_path = sys.argv[1] if len(sys.argv) > 2 else "wine"
    emulator_tool_name = sys.argv[2] if len(sys.argv) > 2 else "wine"

    walk_tests(emulator_tool_path, emulator_tool_name)