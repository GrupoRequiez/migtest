# Copyright 2018 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    product_brand_id = fields.Many2one(
        comodel_name='product.brand',
        string='Brand',
    )

    def _from(self):
        from_str = super(AccountInvoiceReport, self)._from()
        from_str += """
        LEFT JOIN product_brand pb ON pb.id = template.product_brand_id
        """
        return from_str

    @api.model
    def _group_by(self):
        group_by_str = super(AccountInvoiceReport, self)._group_by()
        group_by_str += """
        , pb.name
        """
        return group_by_str

    @api.model
    def _sub_select(self):
        sub_select_str = super(AccountInvoiceReport, self)._sub_select()
        sub_select_str += """
        , pb.name as brand
        """
        return sub_select_str

    @api.model
    def _select(self):
        select_str = super(AccountInvoiceReport, self)._select()
        select_str += """
        , pb.name
        """
        return select_str
    # def _select(self):
    #     select_str = super()._select()
    #     select_str += """
    #         , template.product_brand_id as product_brand_id
    #         """
    #     return select_str
    #
    # def _sub_select(self):
    #     select_str = super()._sub_select()
    #     select_str += """
    #         , template.product_brand_id
    #         """
    #     return select_str
    #
    # def _group_by(self):
    #     group_by_str = super()._group_by()
    #     group_by_str += """
    #         , template.product_brand_id
    #         """
    #     return group_by_str
