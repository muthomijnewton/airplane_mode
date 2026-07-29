# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today
from frappe.model.naming import getseries

class RentPayment(Document):
	def validate(self):
		shop = frappe.get_doc("Airport Shop", self.airport_shop)

		if self.amount_paid >= self.rent_amount:
			self.status = 'Paid'

		elif (
			self.amount_paid < self.rent_amount and
			getdate(today()) > getdate(shop.lease_end_date)
		):
			self.status = 'Overdue'

		else:
			self.status = 'Pending'

	def before_insert(self):
		prefix = f"{self.airport_shop}"
		sequence = getseries(prefix, 3)

		self.receipt_number = f"{prefix}-{sequence}"

		my_date = getdate(self.payment_date)

		self.payment_month = my_date.strftime("%B")
		self.payment_year = my_date.year