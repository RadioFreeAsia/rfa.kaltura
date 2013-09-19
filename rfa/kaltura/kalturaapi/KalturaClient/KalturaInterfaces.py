import abc


class IKalturaClientPlugin:
    
    __metaclass__ = abc.ABCMeta

    @staticmethod #see python 3.3 release notes for abstractstatic.
    @abc.abstractmethod
    # @return KalturaClientPlugin        
    def get():
        """Singleton Constructor
           note that this is enforced as a staticmethod
        """
        pass
    
    @abc.abstractmethod    
    # @return array<KalturaServiceBase>    
    def getServices(self):
        """Insert Docstring here"""
        pass
        
    @abc.abstractmethod
    # @return string
    def getName(self):
        """Insert Docstring Here"""
        pass
    
    