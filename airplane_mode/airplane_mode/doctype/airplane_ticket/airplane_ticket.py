# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class AirplaneTicket(Document):
	def validate(self):
		self.remove_duplicate_add_ons()
		self.calculate_total_amount()

	def before_submit(self):
		if self.status != 'Boarded':
			frappe.throw("Only boarded tickets can be submitted")

	def remove_duplicate_add_ons(self):
		unique_items = []
		seen = set()

		for add_on in self.add_ons:
			if add_on.item not in seen:
				seen.add(add_on.item)
				unique_items.append(add_on)

		self.add_ons = unique_items

	def calculate_total_amount(self):
		total = self.flight_price

		for add_on in self.add_ons:
			total += add_on.amount or 0

		self.total_amount = total
