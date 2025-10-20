# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo import http
from odoo.http import request
from datetime import date
import calendar, math, re, io, base64, os, json, werkzeug

import logging

_logger = logging.getLogger(__name__)


class DslStudyStudentResult(models.Model):
    _name = "dsl.study.student.result"
    _description = "Student Academic Result"

    # Basic info
    exam_type = fields.Selection(
        [
            ("ssc", "SSC"),
            ("hsc", "HSC"),
            ("o_level", "O-level"),
            ("a_level", "A-level"),
            ("diploma", "Diploma"),
            ("bachelor", "Bachelor"),
            ("masters", "Masters"),
            ("others", "Others"),
        ],
        string="Exam Type",
        required=True,
    )

    institution_name = fields.Char(string="Institution Name")
    institution_code = fields.Char(string="Institution Code")
    department = fields.Char(string="Department")
    education_board_id = fields.Many2one(
        "dsl.study.education.board", string="Education Board"
    )
    group_or_major = fields.Char(string="Group / Major")

    grade = fields.Selection(
        [
            ("first", "First Division"),
            ("second", "Second Division"),
            ("pass", "Pass"),
            ("gpa", "GPA"),
            ("others", "Others"),
        ],
        string="Grade",
    )

    grade_point = fields.Float(string="Grade Point")
    total_mark = fields.Integer(string="Total Mark")
    passing_year = fields.Char(string="Passing Year")
    duration_year = fields.Selection(
        [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5")],
        string="Duration (Years)",
    )

    marksheet = fields.Binary(string="Marksheet")
    certificate = fields.Binary(string="Certificate")
    board_roll_number = fields.Char(string="Board Roll Number")
    registration_number = fields.Char(string="Registration Number")

    # common
    note = fields.Text(string="Notes")
    code = fields.Char(string="Code", default="New", readonly=True, copy=False)
    active = fields.Boolean(default=True)

    # Relationship to student
    student_id = fields.Many2one(
        comodel_name="dsl.study.student",
        string="Student",
        required=True,
        ondelete="cascade",
    )

    def toggle_active(self):
        for rec in self:
            rec.active = not rec.active

    @api.model
    def create(self, vals):
        if vals.get("code", "New") == "New":
            vals["code"] = (
                self.env["ir.sequence"].next_by_code("dsl.study.result.code") or "New"
            )
        return super().create(vals)
