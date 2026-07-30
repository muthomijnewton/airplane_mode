# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class AirportShop(WebsiteGenerator):
	def validate(self):
		self.route = frappe.scrub(self.name)

	def before_insert(self):
		if not self.monthly_rent:
			self.monthly_rent = frappe.db.get_single_value(
				"Airport Shop Settings",
				"default_rent_amount"
			)
