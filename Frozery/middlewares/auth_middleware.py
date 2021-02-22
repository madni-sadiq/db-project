from django.shortcuts import redirect


def auth_middleware(get_response):

    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        Customer = request.session.get('Customer')
        admin = request.session.get('admin')
        if (not Customer) and (not admin):
            return redirect(f'/accounts/login?return_url={returnUrl}')
        
        response = get_response(request)

        return response

    return middleware