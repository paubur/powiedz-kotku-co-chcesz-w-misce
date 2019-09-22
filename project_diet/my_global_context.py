from datetime import datetime
from django.utils import timezone as tz

def get_version_and_time_context(request):
    version = (1,0)
    time = datetime.now()
    return {'version':version, 'time':time}

