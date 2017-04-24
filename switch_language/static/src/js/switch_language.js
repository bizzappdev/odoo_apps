odoo.define('switch_language.SwitchLanguageMenu', function(require) {
"use strict";

var Model = require('web.Model');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var SwitchLanguageMenu = Widget.extend({
    template: 'SwitchLanguageMenu',
    willStart: function() {
        var self = this;
        
        var ret_val = this._super();
        return new Model('res.lang').call('search_read', [[], ['name', 'code']]).then(function (res){
            if (res.length > 1){
                return ret_val;
            }
            else{
                return $.Deferred().reject();
            }
        });
    },
    start: function() {
        var self = this;
        this.$el.on('click', '.dropdown-menu li a[data-menu]', _.debounce(function(ev) {
            ev.preventDefault();
            var lang = $(ev.currentTarget).data('lang-id');
            new Model('res.users').call('write', [[session.uid], {'lang': lang}]).then(function() {
                location.reload();
            });
        }, 1500, true));

        self.$('.oe_topbar_name').text("Language");
        var lang_list = '';
        new Model('res.lang').call('search_read', [[], ['name', 'code']]).then(function (res){
            _.each(res, function(lang) {
                var a = '';
                if (lang['code'] === session.user_context.lang) {
                    self.$('.oe_topbar_name').text(lang['name']);
                    a = '<i class="fa fa-check o_current_company"></i>';
                } else {
                    a = '<span class="o_company"/>';
                }
                lang_list += '<li><a href="#" data-menu="lang" data-lang-id="' + lang['code'] + '">' + a + lang['name'] + '</a></li>';
            });
            
            self.$('.dropdown-menu').html(lang_list);
        });
        return this._super();
    },
});

SystrayMenu.Items.push(SwitchLanguageMenu);

});
