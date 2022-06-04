from django.shortcuts import render
# from django.contrib.auth.decorators import login_required # TODO
from django.views.decorators.http import require_GET, require_POST # TODO
from .__version__ import __version__ as se_version # TODO

# from django.conf import settings # TODO

@require_GET
def pidtuningtool(request):
    context = {
    }
    return render(request, 'pidtuningtool/index.html', context)
