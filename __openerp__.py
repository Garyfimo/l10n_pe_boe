# -*- encoding: utf-8 -*-
#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 OSSE Soluciones - Oficina de Soluciones y Servicios Empresariales
#    http://www.osse.com.pe
#
#    WARNING: This program as such is intended to be used by professional
#    programmers who take the whole responsability of assessing all potential
#    consequences resulting from its eventual inadequacies and bugs
#    End users who are looking for a ready-to-use solution with commercial
#    garantees and support are strongly adviced to contract a Free Software
#    Service Company
#
#    This program is Free Software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#########################################################################################
{
    "name": "Peruvian Accounting Localization - Bill of Exchange",
    "version": "1.0",
    "description": """
Canje de Facturas por Letras
    """,
    "author": "OSSE Soluciones",
    "website": "http://www.osse.com.pe",
    "category": "Localisation/Profile",
    "depends": [
        "account",
	],
    "data":[
#          "security/ir.model.access.csv",
#          "security/security.xml",
          "view/bill_of_exchange_supplier_view.xml",
          "view/bill_of_exchange_customer_view.xml",
          "data/account_data.xml",
          #"wizard/create_boe_view.xml"
	],
    "demo_xml": [
	],
    "update_xml": [
	],
    "active": False,
    "installable": True,
    "certificate" : "",
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
