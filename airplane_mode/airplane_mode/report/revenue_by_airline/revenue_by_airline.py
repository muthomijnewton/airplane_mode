# Copyright (c) 2026, Newton Muthomi and contributors
# For license information, please see license.txt

import frappe
from frappe.query_builder import DocType
from pypika.functions import Sum


def execute(filters=None):
	columns = [
		{
			"label": "Airline",
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline",
			"width": 250,
		},

		{
			"label": "Revenue",
			"fieldname": "revenue",
			"fieldtype": "Currency",
			"width": 150,
		},
	]

	Airline = DocType('Airline')
	Airplane = DocType("Airplane")
	AirplaneFlight = DocType("Airplane Flight")
	AirplaneTicket = DocType("Airplane Ticket")

	results = (
		frappe.qb
		.from_(Airline)
		.left_join(Airplane)
			.on(Airplane.airline == Airline.name)
		.left_join(AirplaneFlight)
			.on(AirplaneFlight.airplane == Airplane.name)
		.left_join(AirplaneTicket)
			.on(
				(AirplaneTicket.flight == AirplaneFlight.name) &
				(AirplaneTicket.docstatus == 1)
			)
		.select(
			Airline.name.as_("airline"),
			Sum(AirplaneTicket.total_amount).as_("revenue")
		)
		.groupby(Airline.name)
	).run(as_dict=True)

	data = []
	total_revenue = 0

	for row in results:
		revenue = row.revenue or 0
		total_revenue += revenue

		data.append({
			"airline":row.airline,
			"revenue": revenue
		})

	data.sort(key=lambda x: x["revenue"], reverse=True)

	chart = {
		"data": {
			"labels":[d["airline"] for d in data],
			"datasets": [
				{
					"values": [d["revenue"] for d in data]
				}
			]
		},
		"type": "donut"
	}

	report_summary = [
		{
			"label": "Total Revenue",
			"value": total_revenue,
			"datatype": "Currency",
			"indicator": "Green",
		}
	]

	return columns, data, None, chart, report_summary

def execute_snapshot_report(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for snapshot report. When 'Synced
	Report' is enabled in report, framework will call this method
	every time the report is refreshed or a filter is updated. It
	accepts the same filters as normal execute. But a utility method -
	get_latest_sync, is also imported.

	"""
	from frappe.database.duckdb.database import get_latest_sync

	columns, data = [], []
	return columns, data
