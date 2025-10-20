# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo import http
from odoo.http import request
from datetime import date
import calendar, math, re, io, base64, os, json, werkzeug

import logging
_logger = logging.getLogger(__name__)

class DslStudyEducationBoard(models.Model):
    _name = "dsl.study.education.board"
    _description = "Education Board"

    # Board name 
    name = fields.Char(string="Board Name", required=True)



    # Country of the board
    # country_id = fields.Many2one("res.country", string="Country")

    # Relations to see all results linked to this board, nishans extras 
    result_ids = fields.One2many(
        comodel_name="dsl.study.student.result",
        inverse_name="education_board_id",
        string="Results"
    )
