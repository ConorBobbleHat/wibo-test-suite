import sys
import os
import django

# We want to use a bunch of utilities defined in the decomp.me repo for our own nefarious purposes
# However: django requires a lot of coaxing to be able to used in any sort of library-like form
# These few lines inject the decomp.me backend onto the pypath, and does all the required setup to keep django happy
sys.path.insert(0, "decomp.me/backend")
os.environ["DJANGO_SETTINGS_MODULE"] = "decompme.settings"
django.setup()