from odoo import fields, models, api
from odoo.addons.hr_payroll.models.browsable_object import BrowsableObject, InputLine, WorkedDays, Payslips


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    def get_all_rules(self, payslip, localdict):
        return self.rule_ids, localdict


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def _prepare_payslip_line_vals(self, contract, rule, amount, qty, rate, localdict):
        return {
            'sequence': rule.sequence,
            'code': rule.code,
            'name': rule.name,
            'note': rule.note,
            'salary_rule_id': rule.id,
            'contract_id': contract.id,
            'employee_id': contract.employee_id.id,
            'amount': amount,
            'quantity': qty,
            'rate': rate,
            'slip_id': self.id,
        }

    def _get_payslip_lines(self):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = localdict['categories'].dict.get(category.code, 0) + amount
            return localdict

        self.ensure_one()
        result = {}
        rules_dict = {}
        worked_days_dict = {line.code: line for line in self.worked_days_line_ids if line.code}
        inputs_dict = {line.code: line for line in self.input_line_ids if line.code}

        employee = self.employee_id
        contract = self.contract_id

        localdict = {
            **self._get_base_local_dict(),
            **{
                'categories': BrowsableObject(employee.id, {}, self.env),
                'rules': BrowsableObject(employee.id, rules_dict, self.env),
                'payslip': Payslips(employee.id, self, self.env),
                'worked_days': WorkedDays(employee.id, worked_days_dict, self.env),
                'inputs': InputLine(employee.id, inputs_dict, self.env),
                'employee': employee,
                'contract': contract
            }
        }

        rules, localdict = self.struct_id.get_all_rules(self,localdict)
        # run the rules by sequence
        # for rule in sorted(self.struct_id.rule_ids, key=lambda x: x.sequence):
        for rule in sorted(rules, key=lambda x: x.sequence):
            localdict.update({
                'result': None,
                'result_qty': 1.0,
                'result_rate': 100})
            if rule._satisfy_condition(localdict):
                amount, qty, rate = rule._compute_rule(localdict)
                #check if there is already a rule computed with that code
                previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                #set/overwrite the amount computed for this rule in the localdict
                tot_rule = amount * qty * rate / 100.0
                localdict[rule.code] = tot_rule
                rules_dict[rule.code] = rule
                # sum the amount for its salary category
                localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                # create/overwrite the rule in the temporary results
                result[rule.code] = self._prepare_payslip_line_vals(contract, rule, amount, qty, rate, localdict)

        return result.values()
