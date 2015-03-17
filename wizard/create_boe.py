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

from osv import osv, fields

class CreateBoEWizard(osv.TransientModel):
	_name = 'l10n_pe.create.boe.wizard'
	_columns = {
		'invoice_id' : fields.many2one('account.invoice', required=True),
		'boe_ids' : fields.one2many("l10n_pe.boe.wizard", 'wizar_id', string="BOEs"),
	}


class BoEWizard(osv.TransientModel):
	_name = 'l10n_pe.boe.wizard'

	_columns = {
		'invoice_by_boe' : fields.many2one("l10n_pe.invoice_by_boe", 'Invoice by BoE', required=True),
		'wizard_id' : fields.many2one('l10n_pe.create.boe.wizard'),
	}