from Products.CMFCore.utils import getToolByName

default_profile = 'profile-rfa.kaltura:default'

def upgrade(upgrade_product,version): 
    """ Decorator for updating the QuickInstaller of a upgrade """
    def wrap_func(fn):
        def wrap_func_args(context,*args):
            p = getToolByName(context,'portal_quickinstaller').get(upgrade_product)
            setattr(p,'installedversion',version)
            return fn(context,*args)
        return wrap_func_args
    return wrap_func


def upgrade_to_1001(context):
    print "Upgrading to 1001"
    context.runImportStepFromProfile(default_profile, 'registry')