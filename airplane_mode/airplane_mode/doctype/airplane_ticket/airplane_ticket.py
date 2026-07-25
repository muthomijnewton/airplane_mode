# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt
import math
from random import choice

import frappe
from frappe import _
from frappe.model.document import Document


class AirplaneTicket(Document):
	def before_insert(self):
		self.assign_seat()

	def assign_seat(self):
		capacity = frappe.db.get_value(
			"Airplane",
			self.flight,
			"capacity"
		)

		if not capacity:
			frappe.throw('The selected airplane does not have a valid capacity.')

		seat_letters = ['A', 'B', 'C', 'D', 'E']
		seats_per_row = len(seat_letters)

		available_seats = []

		for seat_index in range(capacity):
			row = (seat_index // seats_per_row) + 1
			letter = seat_letters[seat_index % seats_per_row]
			available_seats.append(f"{row}{letter}")

		booked_seats = frappe.get_all(
			'Airplane Ticket',
			filters = {
				'flight': self.flight
			},
			pluck = 'seat'
		)

		booked_seats = set(booked_seats)

		available_seats = [
			seat for seat in available_seats
			if seat not in booked_seats
		]

		if not available_seats:
			frappe.throw(_('This flight is fully booked.'))

		self.seat = choice(available_seats)

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
