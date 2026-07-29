import frappe
from frappe.utils import getdate, today
from calendar import month_name


def send_rent_reminders():

    # Only send reminders on the first day of each month.
    current_date = getdate(today())

    if current_date.day != 1:
        return

    # Determine which month's rent should now be overdue.
    if current_date.month == 1:
        overdue_month = "December"
        overdue_year = current_date.year - 1
    else:
        overdue_month = month_name[current_date.month - 1]
        overdue_year = current_date.year

    overdue_payments = frappe.get_all(
        "Rent Payment",
        filters={
            "status": "Overdue",
            "payment_month": overdue_month,
            "payment_year": overdue_year,
            "docstatus": 1
        },
        fields=[
            "name",
            "airport_shop",
            "tenant",
            "amount_paid"
        ]
    )

    reminders_sent = 0

    for payment in overdue_payments:

        tenant = frappe.db.get_value(
            "Shop Tenant",
            payment.tenant,
            ["tenant_name", "tenant_email"],
            as_dict=True
        )

        if not tenant or not tenant.tenant_email:
            continue

        frappe.sendmail(
            recipients=[tenant.tenant_email],
            subject=f"Rent Payment Reminder - {overdue_month} {overdue_year}",
            message=f"""
Dear {tenant.tenant_name},

This is a friendly reminder that your rent payment for <b>{overdue_month} {overdue_year}</b>
for Shop <b>{payment.airport_shop}</b> is currently <b>Overdue</b>.

Amount Due:
<b>KES {payment.amount_paid:,.2f}</b>

Kindly make payment as soon as possible to avoid penalties.

If you have already made your payment, please ignore this email or contact the Airport Management Office.

Regards,<br><br>
Airport Shop Management
"""
        )

        reminders_sent += 1

    frappe.logger().info(
        f"{reminders_sent} rent reminder(s) sent for {overdue_month} {overdue_year}"
    )