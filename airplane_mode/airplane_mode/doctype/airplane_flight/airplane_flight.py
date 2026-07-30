# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class AirplaneFlight(WebsiteGenerator):
	def on_update(self):

		if self.has_value_changed("gate_number"):
			frappe.enqueue(
				"airplane_mode.airplane_mode.jobs.update_ticket_gate_numbers",
				queue = "short",
				flight_name = self.name,
				gate_number= self.gate_number
			)

	def on_submit(self):
		self.db_set('status', 'Completed')
