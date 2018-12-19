import os

fileDir = os.path.dirname(os.path.abspath(__file__))
ouputDir = os.path.dirname(fileDir)

def collect_coverage(function):
    def wrapper(*args, **kwargs):
        import coverage
        cov = coverage.Coverage(data_file=f"{ouputDir}.coverage-{function.__name__}")
        cov.start()
        result = function(*args, **kwargs)
        cov.stop()
        cov.save()
        return result
    return wrapper

def coverageCollector(TestClass):
    class TestClassWithCoverage(TestClass):
        def __init__(self,*args,**kwargs):
            self.oInstance = TestClass(*args, **kwargs)

        def __getattribute__(self, attr):
            """ this is called whenever any attribute of a NewCls object is accessed. This function first tries to 
                get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
                instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and 
                the attribute is an instance method then `time_this` is applied. """
            try:
                method = super(TestClassWithCoverage, self).__getattribute__(attr)
            except AttributeError:
                pass  # Nothing needs to be done if the method doesn't exist
            else:
                return method 
            method = self.oInstance.__getattribute__(attr)
            if type(method) == type(self.__init__):  # Check we're calling instance methods (all test methods should be).
                return collect_coverage(method)
            else
                return method
    return TestClassWithCoverage
        