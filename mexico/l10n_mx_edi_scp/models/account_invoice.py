
from lxml import etree
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_property = fields.Many2one(
        'res.partner', 'Address Property in Construction',
        help='Use this field when the invoice require the '
        'complement to "Partial construction services". This value will be '
        'used to indicate the information of the property in which are '
        'provided the partial construction services.')

    def _l10n_mx_edi_create_cfdi(self):
        """If the CFDI was signed, try to adds the schemaLocation for Donations"""
        result = super(AccountMove, self)._l10n_mx_edi_create_cfdi()
        cfdi = result.get('cfdi')
        if not cfdi:
            return result
        cfdi = self.l10n_mx_edi_get_xml_etree(cfdi)
        if 'servicioparcial' not in cfdi.nsmap:
            return result
        cfdi.attrib['{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'] = '%s %s %s' % (
            cfdi.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation'),
            'http://www.sat.gob.mx/servicioparcialconstruccion',
            'http://www.sat.gob.mx/sitio_internet/cfd/servicioparcialconstruccion/servicioparcialconstruccion.xsd')
        result['cfdi'] = etree.tostring(cfdi, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        return result
