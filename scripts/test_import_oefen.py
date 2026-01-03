import importlib
try:
    mod = importlib.import_module('app.events.oefen')
    print('imported oefen:', mod)
except Exception as e:
    print('import error:', type(e), e)
