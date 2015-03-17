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

from openerp.osv import fields, osv
from openerp.tools.translate import _

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'invoice_by_boe_id' : fields.one2many("l10n_pe.invoice_by_boe", "invoice_id", string="Bill of exchange payment", readonly=True),
    }
    
class res_partner(osv.Model):
    _inherit = "res.partner"    
    _columns = {
        'partner_by_boe_id' : fields.one2many("l10n_pe.partner_by_boe", "partner_id", string="Bill of exchange partner", readonly=True),
    }

class partner_by_boe(osv.Model):
    _name = "l10n_pe.partner_by_boe"
    _description = "Partner by Bill of exchange"

    _columns = {
        #'name' : fields.char("Aval name", help="Nombre del AVAL de la Letra")
        'partner_id' : fields.many2one('res.partner', 'Aval', required=True, ondelete="cascade", help="Aval de la letra."),
        'boe_id' : fields.many2one('l10n_pe.boe', 'Bill of exchange', ondelete="cascade", help="Referencia de la letra de cambio."),
    }


class invoice_by_boe(osv.Model):
    _name = "l10n_pe.invoice_by_boe"
    _description = "Invoice by Bill of exchange"    

    _columns = {
        'amount' : fields.float("Amount", digits=(12,2), help="Monto pagado de la factura."),
        'invoice_id' : fields.many2one('account.invoice', 'Invoice', required=True, ondelete="cascade", help="Referencia de la factura."),
        'boe_id' : fields.many2one('l10n_pe.boe', 'Bill of exchange', ondelete="cascade", help="Referencia de la letra de cambio."),
        'percent' : fields.float('Percent', digits=(12, 2),readonly=True, help="Porcentaje pagado de la factura.")
    }

    def onchange_invoice(self, cr, uid, ids, invoice_id=False, context=None):
        res = {}
        print invoice_id
        if invoice_id:
            invoice = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=context)
            res['amount'] = invoice.amount_total
            print "Total de factura : %s" % str(invoice.amount_total)
 
        return {'value' : res}


class bill_of_exchange(osv.Model):
    _name = "l10n_pe.boe"
    _description = 'Bill of exchange'
    _order = "id desc"         

    _columns = {
 		'name': fields.char('Description', required=True),
        'partner_id': fields.many2one('res.partner', 'Partner',required=True, ondelete="cascade"),
 		'invoice_by_boe_id' : fields.one2many("l10n_pe.invoice_by_boe", 'boe_id', string="Invoices"),
        'partner_by_boe_id' : fields.one2many("l10n_pe.partner_by_boe", 'boe_id', string="Avales"),
        'type': fields.selection([
            ('out_boe','Customer Bill of Exchange'),
            ('in_boe','Supplier Bill of Exchange'),
            ('out_refund','Customer Refund'),
            ('in_refund','Supplier Refund'),
            ],'Type', select=True, change_default=True, track_visibility='always'),
        'company_id': fields.many2one('res.company', 'Company', required=False, states={'draft':[('readonly',False)]}, visible=False),
        'state': fields.selection([
            ('draft','Draft'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ],'Status', select=True, readonly=True, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Invoice. \
            \n* The \'Open\' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice. \
            \n* The \'Paid\' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled. \
            \n* The \'Cancelled\' status is used when user cancel invoice.'),
        'amount' : fields.float('Amount', digits=(12,2), help="Monto de la letra de cambio."),
 		'date' : fields.date('Creation Date', help="Fecha de canje de la letra de cambio."),
 		'date_due' : fields.date('Due Date', help="Fecha de vencimiento de la letra de cambio."),
 		'journal_id' : fields.many2one('account.journal', 'Journal', required=True, states={'draft':[('readonly',False)]}),
                                      #domain="[('type', 'in', {'out_invoice': ['sale'], 'out_refund': ['sale_refund'], 'in_refund': ['purchase_refund'], 'in_invoice': ['purchase']}.get(type, [])), ('company_id', '=', company_id)]"),
 		'account_id' : fields.many2one('account.account', 'Account',required=True, domain=[('type','<>','view'), ('type', '<>', 'closed')], help="Cuenta donde se pagará la letra de cambio."),
        'period_id' : fields.many2one('account.period','Period', required=True,states={'draft':[('readonly',False)]}),

 	}
    _defaults = {
        'state' : 'draft',
        'date' : fields.date.today,
    }

    def _get_reverse_lines(self, cr, uid, expense_invoice, lines, context=None):
        res = []
        for line in lines:
            l = {'name': line.name,
                'partner_id': line.partner_id.id,
                'account_id': line.account_id.id,
                'debit': line.credit,
                'credit': line.debit,
                'amount_currency': line.amount_currency * -1,
                'currency_id': line.currency_id.id,
                'invoice': line.invoice.id,
                }
            res.append((0,0,l))
            l1 = l.copy()
            l1['partner_id'] = expense_invoice.expense_id.partner_id.id
            l1['debit'] = line.debit
            l1['credit'] = line.credit
            l1['amount_currency'] = line.amount_currency
            res.append((0,0,l1))
        return res

    def _get_reverse_move(self, cr, uid, expense_invoice, move, lines, context=None):
        return {
                'ref': move.ref,
                'line_id': self._get_reverse_lines(cr, uid, expense_invoice, lines, context=context),
                'journal_id': move.journal_id.id,
                'date': move.date,
                'narration': move.narration,
                'period_id': move.period_id.id,
                'company_id': move.company_id.id,
                'expense_id': move.expense_id.id,
            }

    def action_confirm(self, cr, uid, ids, context=None):
        move_obj = self.pool.get('account.move')
        line_obj = self.pool.get('account.move.line')
        journal_obj = self.pool.get('account.journal')
        self.write(cr,uid,ids, {'state' : 'open'})
        for boe in self.browse(cr,uid,ids,context=context):
          #journal_ids = journal_obj.search(cr, uid, [('code','=','BOE'),('company_id','=',boe.company_id.id)])
            
           # print len(boe.invoice_by_boe_id)
            if boe:
                if len(boe.invoice_by_boe_id) == 0:
                    raise osv.except_osv (_('Missing invoice error'),
                       _('No invoice added, must be at least one invoice'))
                else:
                    """ error message 
                    almenos una linea"""
                    #journal = journal_obj.browse(cr, uid, journal_ids[0], context=context)    
                    self.button_update_amount(cr, uid, ids,context=context)
                    res = {
                        'journal_id' : boe.journal_id.id,
                        'period_id' : boe.period_id.id,
                        'ref' : boe.name,
                        'date' : boe.date,
                        'company_id' : boe.company_id.id,
                        }
                    move_id = move_obj.create(cr,uid,res,context=context)

                    res = {
                        'name' : boe.name,
                        'partner_id' : boe.partner_id.id,
                        'account_id' : boe.journal_id.default_debit_account_id.id,
                        'move_id' : move_id,
                        'debit' : 0.00,
                        'credit' : .000,
                    #'amount_currency' : 0.00,
                    }
                    for inv in boe.invoice_by_boe_id:
                        if inv.amount == inv.invoice_id.amount_total:
                            inv.invoice_id.state = "paid"
                            print inv.invoice_id.state
                            print "exito"
                    line_obj.create(cr, uid, res, context=context)

    def button_update_amount(self, cr, uid, ids, context=None):
        vals = {}
        
        print "aqui empieza" 
        total = 0.00
        boes = self.browse(cr,uid,ids,context=context)
        if boes:
            for boe in boes:
                for inv in boe.invoice_by_boe_id:
                    total = total + inv.invoice_id.amount_total
                    
        #print ibb.invoice_by_boe.invoice_id.amount_total
            vals['amount'] = total    
            print total
            print "aqui finaliza"
            self.write(cr,uid,ids,{'amount':total})
            return True
        else:
            return False



