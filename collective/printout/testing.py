from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class CollectivePrintout(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.printout
        xmlconfig.file('configure.zcml', 
                       collective.printout, 
                       context=configurationContext)

        # Install product and call its initialize() function
        #z2.installProduct(app, 'collective.printout')

        # Note: you can skip this if collective.printout is not a Zope 2-style
        # product, i.e. it is not in the Products.* namespace and it
        # does not have a <five:registerPackage /> directive in its
        # configure.zcml.

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'collective.printout:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'collective.printout')

        # Note: Again, you can skip this if collective.printout is not a Zope 
        # 2-style product

COLLECTIVE_PRINTOUT_FIXTURE = CollectivePrintout()
COLLECTIVE_PRINTOUT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PRINTOUT_FIXTURE,), 
    name="Collectiveprintout:Integration")
COLLECTIVE_PRINTOUT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PRINTOUT_FIXTURE,), 
    name="Collectiveprintout:Functional")
