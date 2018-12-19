import os

fileDir = os.path.dirname(os.path.abspath(__file__))
ouputDir = os.path.dirname(fileDir)

def coverageCollector(function):
    def wrapper(*args, **kwargs):
        import coverage
        cov = coverage.Coverage(data_file=f".coverage-{function.__name__}")
        cov.start()
        result = function(*args, **kwargs)
        cov.stop()
        cov.save()
        return result
    return wrapper
        