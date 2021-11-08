import os

if os.environ.get("ZOOM_PRODUCTION") is not None:
    from zoom.settings.production import *
else:
    from zoom.settings.development import *
