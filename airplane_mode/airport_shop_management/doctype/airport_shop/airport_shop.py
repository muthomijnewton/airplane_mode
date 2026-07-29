# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirportShop(Document):
	def before_insert(self):
		if not self.rent_amount:
			self.rent_amount = frappe.db.get_single_value(
				"Airport Shop Settings",
				"default_rent_amount"
			)
