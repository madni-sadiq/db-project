from django.shortcuts import redirect


def auth_middleware(get_response):

    def middleware(request):
        returnUrl = request.META['PATH_INFO']
        Customer = request.session.get('Customer') 
        if not Customer:
            return redirect(f'/accounts/login?return_url={returnUrl}')
        
        response = get_response(request)

        return response

    return middleware