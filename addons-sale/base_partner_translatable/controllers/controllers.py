# -*- coding: utf-8 -*-
# from odoo import http


# class BasePartnerTranslatable(http.Controller):
#     @http.route('/base_partner_translatable/base_partner_translatable/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_partner_translatable/base_partner_translatable/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_partner_translatable.listing', {
#             'root': '/base_partner_translatable/base_partner_translatable',
#             'objects': http.request.env['base_partner_translatable.base_partner_translatable'].search([]),
#         })

#     @http.route('/base_partner_translatable/base_partner_translatable/objects/<model("base_partner_translatable.base_partner_translatable"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_partner_translatable.object', {
#             'object': obj
#         })
