# -*- coding: utf-8 -*-
# Copyright (c) 2021, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class HREmployeeAppraisal(Document):
    def before_insert(self):
        if not self.template:
            return
        template = frappe.get_doc("HR Appraisal Template", self.template)
        for el in template.jobs:
            row = self.append('jobs', {})
            row.title = el.title
            row.description = el.description
        for el in template.performances:
            row = self.append('performances', {})
            row.title = el.title
            row.description = el.description

    def validate(self):
        self.set_totals()
        self.validate_edit()

    def set_totals(self):
        jobs_count = len(self.jobs)
        self.employee_job_total = 0
        self.manager_job_total = 0
        self.panelist_job_total = 0
        if jobs_count > 0:
            for row in self.jobs:
                self.employee_job_total += flt(row.employee_rating)
                self.manager_job_total += flt(row.manager_rating)
                self.panelist_job_total += flt(row.panelist_rating)

            self.employee_job_average = self.employee_job_total / jobs_count
            self.manager_job_average = self.manager_job_total / jobs_count
            self.panelist_job_average = self.panelist_job_total / jobs_count

        performances_count = len(self.performances)
        self.employee_performance_total = 0
        self.manager_performance_total = 0
        self.panelist_performance_total = 0
        if performances_count > 0:
            for elm in self.performances:
                self.employee_performance_total += flt(elm.employee_rating)
                self.manager_performance_total += flt(elm.manager_rating)
                self.panelist_performance_total += flt(elm.panelist_rating)

            self.employee_performance_average = self.employee_performance_total / performances_count
            self.manager_performance_average = self.manager_performance_total / performances_count
            self.panelist_performance_average = self.panelist_performance_total / performances_count

        self.employee_total = self.employee_job_total + self.employee_performance_total
        self.employee_average = (
            self.employee_job_average + self.employee_performance_average) / 2
        self.manager_total = self.manager_job_total + self.manager_performance_total
        self.manager_average = (
            self.manager_job_average + self.manager_performance_average) / 2
        self.panelist_total = self.panelist_job_total + self.panelist_performance_total
        self.panelist_average = (
            self.panelist_job_average + self.panelist_performance_average) / 2

    def validate_edit(self):
        template = frappe.get_doc("HR Appraisal Template", self.template)
        temp_jobs_count = len(template.jobs)
        jobs_count = len(self.jobs)
        temp_performances_count = len(template.performances)
        performances_count = len(self.performances)
        if temp_jobs_count != jobs_count:
            frappe.throw(
                _("Appraisal Job Details shshould not be added or deleted from any lines"))
        if temp_performances_count != performances_count:
            frappe.throw(
                _("Appraisal Performance Details shshould not be added or deleted from any lines"))
