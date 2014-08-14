
import ZODB.POSException
from zope.interface import implements
from ZODB.interfaces import IStorage

from zope.component.zcml import interface

from zope.interface import Interface
class INoStorage(IStorage):
    pass 


class NoStorage(object):
    """Completely skip storage on Plone.  
       Rely solely on storage remotely on Kaltura Media Center
    """
    implements(INoStorage)
    
    def __init__(self):
        pass 
   
    def close():
        pass

    def getName():
        return "NoStorage - Blackhole"

    def getSize():
        return 0

    def history(oid, size=1):
        return []

    def isReadOnly():
        False
        
    def lastTransaction():
        b"00000000"

    def __len__():
        0

    def load(oid, version):
        """
        A POSKeyError is raised if there is no record for the object id.
        """
        raise ZODB.POSException.POSKeyError

    def loadBefore(oid, tid):
        raise ZODB.POSException.POSKeyError

    def loadSerial(oid, serial):
        raise ZODB.POSException.POSKeyError

    def new_oid():
        return ""
    
    def pack(pack_time, referencesf):
        pass #that was easy!

    def registerDB(wrapper):
        pass

    def sortKey():
        return ""

    def store(oid, serial, data, version, transaction):
        import pdb; pdb.set_trace()
        pass   

    def tpc_abort(transaction):
        pass

    def tpc_begin(transaction):
        pass

    def tpc_finish(transaction, func = lambda tid: None):
        pass

    def tpc_vote(transaction):
        pass

    