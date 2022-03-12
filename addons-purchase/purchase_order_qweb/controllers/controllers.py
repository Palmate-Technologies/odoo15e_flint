# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseOrderQweb(http.Controller):
#     @http.route('/purchase_order_qweb/purchase_order_qweb', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_order_qweb/purchase_order_qweb/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_order_qweb.listing', {
#             'root': '/purchase_order_qweb/purchase_order_qweb',
#             'objects': http.request.env['purchase_order_qweb.purchase_order_qweb'].search([]),
#         })

#     @http.route('/purchase_order_qweb/purchase_order_qweb/objects/<model("purchase_order_qweb.purchase_order_qweb"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_order_qweb.object', {
#             'object': obj
#         })
