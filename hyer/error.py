class HTTPError(Exception):
	''' Error when http reading'''
	pass
class HTTP404Error(HTTPError):
	'''404:not found'''
	pass
class HTTPMaxRedirectsError(HTTPError):
	'''Redirect too many times'''
class HTTPServerInternalError(HTTPError):
	'''50x error,such as:
		 there is somethin wrong with a php file ,so the page can't be displayed
		'''
class HTTPForbiddenError(HTTPError):
	'''403,404...Forbidden'''

class ExitLoopError(Exception):
    '''
    just give a signal to exit the loop of builders
    '''
    pass
