from proteus import config, Model, Wizard
from trytondjangotest import settings

class TrytonProteus:
    ''' This is a wrapper class that will be used by this django project apps to access proteus and tryton,

        this way we would not have Proteus's config.set_trytond() all over our project and other commonly used features
    '''

    def __init__(self):
        self.config = config.set_trytond(database_type=settings.TRYTON_DB_TYPE, database_name=settings.TRYON_DB)
        self.module = Model.get('ir.module.module')

    def get_all_parties(self):
        ''' returns all parties whose party.id is greater than 0, hence all parties.
        '''
        Party = Model.get('party.party')
        return Party.find([('id', '>', 0)])

    def find_party_by_id(self, party_id):
        Party = Model.get('party.party')
        try:
            return Party.find([('id', '=', int(party_id))])[0]
        except:
            return None

    def get_modules(self):
        '''
        return all the modules that exists on the Tryton Server
        '''
        return  self.module.find([('id', '>', 0)])

    def get_model(self, model_name):
        ''' returns Model if it exist, else returns None
        '''
        return Model.get(model_name, None)

    def get_lang_choices(self):
        Lang = Model.get('ir.lang')
        lang_list = Lang.find([('id', '>', 0)])
        return ((lang.code, lang.name) for lang in lang_list)

    def get_contact_types(self):
        ContactMechanism = Model.get('party.contact_mechanism')
        contact_mechanism_types = ContactMechanism.find([('id', '>', '0')])
        return ((type_name, type_name) for type_name in ["Phone", "Mobile", "E-Mail", "Website", "Skype", "SIP", "IRC", "Jabber", "Other"])

    def delete_party_by_id(self, party_id):
        try:
            party = self.find_party_by_id(party_id)
            party.delete();
            return True;
        except:
            return None

    def install_module(self, module_id):
        (module, )=self.module.find([('id', '=', module_id)])
        self.module.install([module.id], self.config.context)
        Wizard('ir.module.module.install_upgrade').execute('upgrade')

    def uninstall_module(self, module_id):
        (module, )=self.module.find([('id', '=', module_id)])
        self.module.uninstall([module.id], self.config.context)
        Wizard('ir.module.module.uninstall').execute('upgrade')
        
    def get_country_choices(self):
        Country = Model.get('country.country')
        country_list = Country.find([('id', '>', 0)])
        return ((country.code, country.name) for country in country_list)


    def __del__(self):
        self.config = None
