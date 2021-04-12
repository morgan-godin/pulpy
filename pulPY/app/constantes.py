from warnings import warn
import os

RESULTS_PER_PAGE = 2
SECRET_KEY = "uEz8jF53GJVcg4"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)