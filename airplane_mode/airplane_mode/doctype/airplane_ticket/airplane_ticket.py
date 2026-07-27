# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
	
	def validate(self):
			self.remove_duplicate_add_ons()
			self.calculate_total_amount()
			self.check_airplane_capacity()

	def check_airplane_capacity(self):
		airplane = frappe.db.get_value(
			"Airplane Flight",
			self.flight,
			"airplane"
		)

		capacity = frappe.db.get_value(
			"Airplane",
			airplane,
			"capacity"
		)	

		booked_tickets = frappe.db.count(
			"Airplane Ticket",
			filters={
				"flight": self.flight
			}
		)

		if not self.is_new():
			booked_tickets -= 1

		if booked_tickets >= capacity:
			frappe.throw("This flight is fully booked")

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
