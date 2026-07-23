# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Airplane(Document):
	def autoname(self):
		count = frappe.db.count(
			"Airplane",
			{"airline": self.airline}
		) + 1

		self.name = f"{self.airline}-{count:03d}"
