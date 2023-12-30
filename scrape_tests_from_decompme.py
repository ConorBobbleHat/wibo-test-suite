import requests
from tqdm import tqdm

import json
import os
import os.path

import settings

import decompme_backend_path
from coreapp.compilers import _all_compilers

from typing import Any, Dict

def get_wibo_compilers():
    return [i.id for i in _all_compilers if "${WIBO}" in i.cc]

def main():
    # We only care about testing compilers wibo is currently used to run
    wibo_compiler_ids = get_wibo_compilers()

    for compiler in tqdm(wibo_compiler_ids):
        compiler_dir = os.path.join(settings.TESTS_DIR, compiler)
        os.makedirs(compiler_dir, exist_ok=True)
        
        top_n_scratches = requests.get(f"{settings.API_BASE}/scratch?compiler={compiler}").json()["results"][:settings.SCRATCHES_PER_COMPILER]

        for scratch in top_n_scratches:
            # The scratch list view only returns a terse description of the scratch,
            # excluding any actual code. We'll need to fetch the full version for our purposes.
            scratch = requests.get(f"{settings.API_BASE}/scratch/{scratch['slug']}").json()

            # Only save what we need - discard author information, etc.
            test_case = {key: scratch[key] for key in ["compiler", "compiler_flags", "source_code", "context", "diff_flags", "diff_label", "libraries"]}
           
            with open(os.path.join(compiler_dir, scratch["slug"] + ".json"), "w") as f:
                json.dump(test_case, f)
           
        # If not enough scratches using this compiler exist:
        # throw in a super simple test case, just so this compiler received some coverage
        if len(top_n_scratches) < settings.SCRATCHES_PER_COMPILER:
            with open(os.path.join(compiler_dir, "base.json"), "w") as f:
                base_case = {
                    "compiler": compiler,
                    "compiler_flags": "",
                    "source_code": "int func(void) { return 5; }",
                    "context": "",
                    "diff_flags": [],
                    "diff_label": "func",
                    "libraries": []
                }
                
                json.dump(base_case, f)


if __name__ == "__main__":
    main()