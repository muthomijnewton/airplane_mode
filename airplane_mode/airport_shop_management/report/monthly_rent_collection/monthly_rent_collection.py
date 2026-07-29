import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum


def execute(filters=None):

    columns = [
        {
            "label": "Month",
            "fieldname": "payment_month",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Year",
            "fieldname": "payment_year",
            "fieldtype": "Int",
            "width": 100,
        },
        {
            "label": "Total Collected",
            "fieldname": "total_collected",
            "fieldtype": "Currency",
            "width": 180,
        },
    ]

    RentPayment = DocType("Rent Payment")

    data = (
        frappe.qb.from_(RentPayment)
        .select(
            RentPayment.payment_month,
            RentPayment.payment_year,
            Sum(RentPayment.amount_paid).as_("total_collected"),
        )
		.where(RentPayment.docstatus == 1)
		
        .groupby(
            RentPayment.payment_month,
            RentPayment.payment_year,
        )
        .orderby(RentPayment.payment_year)
        .orderby(RentPayment.payment_month)
        .run(as_dict=True)
    )

    total_revenue = sum(row.total_collected for row in data)

    chart = {
        "data": {
            "labels": [
                f"{row.payment_month} {row.payment_year}"
                for row in data
            ],
            "datasets": [
                {
                    "name": "Revenue",
                    "values": [
                        row.total_collected
                        for row in data
                    ],
                }
            ],
        },
        "type": "bar",
    }

    summary = [
        {
            "label": "Total Revenue",
            "value": total_revenue,
            "indicator": "Green",
            "datatype": "Currency",
        }
    ]

    return columns, data, None, chart, summary, True