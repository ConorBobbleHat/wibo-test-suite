# wibo-test-suite
A set of tools to test equivalence between wine and wibo on compiler invocations. They lean heavily on [decomp.me](https://decomp.me)'s set of scratches and bank of compilers to provide material to test with, and [asm-differ](https://github.com/simonlindholm/asm-differ) to ultimately determine that compilers output the same assembly under both tools.

## Usage
### Ground-truth generation (offline)
Run: 
- `setup.sh`: to grab a copy of the decomp.me sources, its dependencies, and compilers.
- `scrape_tests.sh`: to populate the `tests` folder with a handful of scratches from every compiler decomp.me uses wibo to run
- `generate_wine_ground_truth.sh`: to have wine compile every test scratch to an object file for comparison

At this stage, the entire state of the repository should be committed.

### Wibo testing (online)
Inside of a CI, run:
- `setup.sh`: as above.
- `run_compare_wine_wibo.sh <absolute path to compiled wibo binary>`: to have wibo compile all of the tests, and check its output against the ground truth.