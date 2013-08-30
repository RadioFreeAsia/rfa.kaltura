import zope.interface

class IRfaKalturaInstalled(zope.interface.Interface):
    """ A layer specific for this add-on product.

    This interface is referred in browserlayer.xml.

    All views and viewlets register against this layer will appear on
    your Plone site only when the add-on installer has been run.
    """