frappe.ready(function () {

    // Get the URL parameters
    const params = new URLSearchParams(window.location.search);

    // Get the shop parameter
    const shop = params.get("shop");

    if (shop) {

        // Populate the Shop field
        frappe.web_form.set_value("shop", shop);

        // Prevent users from changing it
        frappe.web_form.set_df_property(
            "shop",
            "read_only",
            1
        );
    }

});