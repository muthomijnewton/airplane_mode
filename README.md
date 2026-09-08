# Airplane Mode

**An airport management system built with the Frappe Framework.**

Airplane Mode is a Frappe-based application for managing airport and airline operations through a centralized system. It provides functionality for managing flights, passengers, airline-related records, and airport commercial spaces.

The project is built to demonstrate how real-world airport workflows can be modeled and automated using the Frappe Framework.

## Features

### Airline & Flight Management

* Manage airline records and related information
* Manage aircraft and flight records
* Manage flight passengers
* Manage flight-related information and operations
* Manage airline ticket information

### Ticket Management

* Create and manage airline tickets
* Manage ticket add-ons
* Calculate ticket totals based on flight prices and selected add-ons
* Associate passengers with flights and tickets

### Airport Shop Management

The application includes an **Airport Shop Management** module for managing commercial spaces within an airport.

It provides functionality for:

* Airport shop records
* Shop types and classifications
* Shop tenants
* Shop leads
* Shop rental payments
* Airport shop settings
* Rental payment tracking
* Automated rental-related reminders
* Custom print formats and reports
* Web forms for selected workflows

### Automation

The system includes background jobs and scheduled functionality for tasks such as airport shop-related reminders and other recurring operations.

### Development & Quality

The project uses automated development tools and CI workflows to maintain code quality and reliability.

Configured tools include:

* Ruff
* ESLint
* Prettier
* PyUpgrade
* Frappe Semgrep Rules
* pip-audit
* GitHub Actions

## Technology Stack

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Frappe Framework | Application framework     |
| Python           | Backend logic             |
| JavaScript       | Client-side functionality |
| MariaDB          | Database                  |
| Jinja            | Web templates             |
| GitHub Actions   | Continuous integration    |
| Pre-commit       | Code quality automation   |

## Application Structure

The application is organized into several functional areas:

```text
airplane_mode/
├── airplane_mode/
│   ├── airport_shop_management/
│   │   ├── doctype/
│   │   ├── print_format/
│   │   ├── report/
│   │   ├── web_form/
│   │   ├── jobs.py
│   │   └── reminders.py
│   ├── config/
│   ├── fixtures/
│   ├── patches/
│   ├── public/
│   ├── templates/
│   └── www/
├── .github/
│   └── workflows/
├── pyproject.toml
└── README.md
```

## Requirements

Before installing the application, make sure you have a working Frappe Bench environment.

The application is developed for the Frappe Framework and uses the standard Bench workflow for installation.

## Installation

Clone or fetch the application into your Frappe Bench:

```bash
cd $PATH_TO_YOUR_BENCH

bench get-app https://github.com/muthomijnewton/airplane_mode.git --branch develop
```

Install the application on your site:

```bash
bench --site YOUR_SITE install-app airplane_mode
```

Run migrations:

```bash
bench --site YOUR_SITE migrate
```

Start the development server:

```bash
bench start
```

Replace `YOUR_SITE` with the name of your Frappe site.

## Development

After installing the application, the source code is available under:

```text
apps/airplane_mode/
```

Install the development hooks:

```bash
cd apps/airplane_mode
pre-commit install
```

Run the configured checks manually with:

```bash
pre-commit run --all-files
```

## Testing

The project uses Frappe's testing infrastructure.

Run the application's test suite with:

```bash
bench --site YOUR_SITE run-tests --app airplane_mode
```

This runs the automated tests associated with the application.

## Continuous Integration

GitHub Actions is used to automate project checks.

The CI workflow:

* Installs the application
* Sets up the Frappe environment
* Runs automated tests

The linting/security workflow performs additional checks including:

* Frappe Semgrep Rules
* Dependency vulnerability auditing with `pip-audit`

These checks help identify code-quality issues and potentially vulnerable dependencies before changes are merged.

## Contributing

Contributions, suggestions, bug reports, and improvements are welcome.

Before submitting changes:

1. Create a feature branch.
2. Make your changes.
3. Run the test suite.
4. Run the pre-commit checks.
5. Commit your changes with a clear message.
6. Open a pull request.

For local development, enable the pre-commit hooks:

```bash
cd apps/airplane_mode
pre-commit install
```

## Project Status

This project is under active development.

The current implementation focuses on airport and airline management workflows, with additional functionality being developed and refined over time.

## Future Improvements

Potential future improvements include:

* Expanded airport operational workflows
* Additional passenger and ticketing features
* Enhanced reporting and dashboards
* Improved notification and reminder workflows
* Additional automation
* Expanded role-based permissions
* More comprehensive automated test coverage

## License

This project is licensed under the **MIT License**.

See [`license.txt`](license.txt) for the full license text.
