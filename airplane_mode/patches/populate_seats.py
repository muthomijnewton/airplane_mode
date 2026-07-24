import frappe
import random
import string


def execute():
    flights = frappe.get_all("Airplane Flight", pluck="name")

    for flight in flights:
        tickets = frappe.get_all(
            "Airplane Ticket",
            filters={"flight": flight},
            fields=["name"]
        )

        # Generate every possible seat
        available_seats = [
            f"{number}{letter}"
            for number in range(1, 100)
            for letter in "ABCDE"
        ]

        random.shuffle(available_seats)

        for ticket in tickets:
            if not available_seats:
                frappe.throw(f"No seats left for flight {flight}")

            seat = available_seats.pop()

            frappe.db.set_value(
                "Airplane Ticket",
                ticket.name,
                "seat",
                seat,
                update_modified=False
            )

    frappe.db.commit()