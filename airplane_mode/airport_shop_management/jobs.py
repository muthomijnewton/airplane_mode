import frappe


def update_ticket_gate_numbers(flight_name, gate_number):

    tickets = frappe.get_all(
        "Airplane Ticket",
        filters={
            "flight": flight_name,
            "docstatus": ("!=", 2)   # Ignore cancelled tickets
        },
        fields=["name"]
    )

    for ticket in tickets:
        frappe.db.set_value(
            "Airplane Ticket",
            ticket.name,
            "gate_number",
            gate_number,
            update_modified=False
        )

    frappe.db.commit()