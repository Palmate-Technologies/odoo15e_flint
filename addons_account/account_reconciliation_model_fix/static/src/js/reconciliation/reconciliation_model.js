odoo.define('account_reconciliation_model_fix.StatementModel', function (require) {
"use strict";

var reconciliationModel = require('account.ReconciliationModel');

reconciliationModel.StatementModel.include({

    updateProposition: function (handle, values) {
        var self = this;
        var line = this.getLine(handle);
        var prop = _.last(_.filter(line.reconciliation_proposition, '__focus'));
        if ('to_check' in values && values.to_check === false) {
            // check if we have another line with to_check and if yes don't change value of this proposition
            prop.to_check = line.reconciliation_proposition.some(function(rec_prop, index) {
                return rec_prop.id !== prop.id && rec_prop.to_check;
            });
        }
        if (!prop) {
            prop = this._formatQuickCreate(line);
            line.reconciliation_proposition.push(prop);
        }
        _.each(values, function (value, fieldName) {
            if (fieldName === 'analytic_tag_ids') {
                switch (value.operation) {
                    case "ADD_M2M":
                        // handle analytic_tag selection via drop down (single dict) and
                        // full widget (array of dict)
                        var vids = _.isArray(value.ids) ? value.ids : [value.ids];
                        _.each(vids, function (val) {
                            if (!_.findWhere(prop.analytic_tag_ids, {id: val.id})) {
                                prop.analytic_tag_ids.push(val);
                            }
                        });
                        break;
                    case "FORGET":
                        var id = self.localData[value.ids[0]].ref;
                        prop.analytic_tag_ids = _.filter(prop.analytic_tag_ids, function (val) {
                            return val.id !== id;
                        });
                        break;
                }
            }
            else if (fieldName === 'tax_ids') {
                switch(value.operation) {
                    case "ADD_M2M":
                        prop.__tax_to_recompute = true;
                        var vids = _.isArray(value.ids) ? value.ids : [value.ids];
                        _.each(vids, function(val){
                            if (!_.findWhere(prop.tax_ids, {id: val.id})) {
                                value.ids.price_include = self.taxes[val.id] ? self.taxes[val.id].price_include : false;
                                prop.tax_ids.push(val);
                            }
                        });
                        break;
                    case "FORGET":
                        prop.__tax_to_recompute = true;
                        var id = self.localData[value.ids[0]].ref;
                        // Tax tag ids to be removed based on tax removed
                        var to_remove_tax_tag_ids = [];
                        if (prop.tax_tag_ids) {
                            _.each(prop.tax_tag_ids, function(tids) {to_remove_tax_tag_ids.push(tids.id); })
                        }

                        prop.tax_ids = _.filter(prop.tax_ids, function (val) {
                            return val.id !== id;
                        });
                        if (to_remove_tax_tag_ids) {
                            prop.tax_tag_ids = _.filter(prop.tax_tag_ids, function (val) {
                                return to_remove_tax_tag_ids.indexOf(val.id) == -1;
                            });
                        }
                        break;
                }
            }
            else {
                prop[fieldName] = values[fieldName];
            }
        });
        if ('account_id' in values) {
            prop.account_code = prop.account_id ? this.accounts[prop.account_id.id] : '';
        }
        if ('amount' in values) {
            prop.base_amount = values.amount;
        }
        if ('name' in values || 'force_tax_included' in values || 'amount' in values || 'account_id' in values) {
            prop.__tax_to_recompute = true;
        }
        line.createForm = _.pick(prop, this.quickCreateFields);
        // If you check/uncheck the force_tax_included box, reset the createForm amount.
        if(prop.base_amount)
            line.createForm.amount = prop.base_amount;
        if (!prop.tax_ids || prop.tax_ids.length !== 1 ) {
            // When we have 0 or more than 1 taxes, reset the base_amount and force_tax_included, otherwise weird behavior can happen
            prop.amount = prop.base_amount;
            line.createForm.force_tax_included = false;
        }
        return this._computeLine(line);
    },


});

});