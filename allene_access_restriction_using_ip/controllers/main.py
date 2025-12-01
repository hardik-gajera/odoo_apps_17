# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import main
from odoo.http import request
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http


class Home(main.Home):

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            oldUid = request.uid
            remote_ip_address = request.httprequest.environ['REMOTE_ADDR']
            if request.params['login']:
                userObj = request.env['res.users'].sudo().search(
                    [('login', '=', request.params['login'])])
                if userObj.allowed_ips:
                    ip_addr_list = []
                    for rec in userObj.allowed_ips:
                        ip_addr_list.append(rec.ip_address)
                    if remote_ip_address in ip_addr_list:
                        try:
                            uid = request.session.authenticate(
                                request.session.db,
                                request.params[
                                    'login'],
                                request.params[
                                    'password'])
                            request.params['login_success'] = True
                            return request.redirect(
                                self._login_redirect(uid, redirect=redirect))
                        except odoo.exceptions.AccessDenied as e:
                            request.uid = oldUid
                            if e.args == odoo.exceptions.AccessDenied().args:
                                values['error'] = _("Wrong login/password")
                    else:
                        request.uid = oldUid
                        values['error'] = _("This IP address is not allowed to login")
                else:
                    try:
                        uid = request.session.authenticate(request.session.db,
                                                           request.params[
                                                               'login'],
                                                           request.params[
                                                               'password'])
                        request.params['login_success'] = True
                        return request.redirect(
                            self._login_redirect(uid, redirect=redirect))
                    except odoo.exceptions.AccessDenied as e:
                        request.uid = oldUid
                        if e.args == odoo.exceptions.AccessDenied().args:
                            values['error'] = _("Wrong login/password")

        return request.render('web.login', values)
