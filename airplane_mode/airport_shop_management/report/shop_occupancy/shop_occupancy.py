import frappe
from frappe.query_builder import DocType
from frappe.query_builder.functions import Sum, Count
from pypika import Case
from pypika.enums import Order


def execute(filters=None):

    columns = get_columns()
    data = get_data()

    total_available = sum(row.available_shops for row in data)
    total_occupied = sum(row.occupied_shops for row in data)
    total_shops = sum(row.total_shops for row in data)

    occupancy_rate = (
        round((total_occupied / total_shops) * 100, 2)
        if total_shops else 0
    )

    chart = {
        "data": {
            "labels": [row.airport for row in data],
            "datasets": [
                {
                    "name": "Available",
                    "values": [row.available_shops for row in data],
                },
                {
                    "name": "Occupied",
                    "values": [row.occupied_shops for row in data],
                },
            ],
        },
        "type": "bar",
    }

    summary = [
        {
            "label": "Available Shops",
            "value": total_available,
            "datatype": "Int",
            "indicator": "Green",
        },
        {
            "label": "Occupied Shops",
            "value": total_occupied,
            "datatype": "Int",
            "indicator": "Blue",
        },
        {
            "label": "Occupancy Rate",
            "value": occupancy_rate,
            "datatype": "Percent",
            "indicator": "Orange",
        },
    ]

    return columns, data, None, chart, summary, True


def get_columns():

    return [
        {
            "label": "Airport",
            "fieldname": "airport",
            "fieldtype": "Link",
            "options": "Airport",
            "width": 180,
        },
        {
            "label": "Available Shops",
            "fieldname": "available_shops",
            "fieldtype": "Int",
            "width": 160,
        },
        {
            "label": "Occupied Shops",
            "fieldname": "occupied_shops",
            "fieldtype": "Int",
            "width": 160,
        },
        {
            "label": "Total Shops",
            "fieldname": "total_shops",
            "fieldtype": "Int",
            "width": 150,
        },
    ]


def get_data():

    Shop = DocType("Airport Shop")

    available = (
        Case()
        .when(Shop.status == "Available", 1)
        .else_(0)
    )

    occupied = (
        Case()
        .when(Shop.status == "Occupied", 1)
        .else_(0)
    )

    return (
        frappe.qb
        .from_(Shop)
        .select(
            Shop.airport,
            Sum(available).as_("available_shops"),
            Sum(occupied).as_("occupied_shops"),
            Count(Shop.name).as_("total_shops"),
        )
        .groupby(Shop.airport)
        .orderby(Shop.airport, order=Order.asc)
        .run(as_dict=True)
    )