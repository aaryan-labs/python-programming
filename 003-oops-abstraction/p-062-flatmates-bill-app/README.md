# Flatmates Bill App

A Python application that helps two flatmates split an electricity bill fairly based on the number of days each person stayed in the house during the billing period.

This project was built as part of my Object-Oriented Programming (OOP) learning journey and demonstrates how real-world problems can be modeled using classes, attributes, and methods.

## Features

- Fair electricity bill splitting
- Day-based bill calculation
- Command-line interface (CLI)
- PDF report generation
- Object-Oriented design
- Separation of business logic and reporting logic

## Project Structure

```text
p-061-flatmates-bill-app/
│
├── main.py
├── bill.py
├── flatmate.py
├── pdfreport.py
│
├── README.md
│
└── docs/
    ├── application-usage.md
    ├── application-design.md
    └── architecture.md
```

## Documentation

Detailed documentation is available in:

- [Application Usage](docs/application-usage.md)
- [Application Design](docs/application-design.md)
- [Architecture](docs/architecture.md)

## Example Workflow

1. Enter the bill amount.
2. Enter the billing period.
3. Enter details for both flatmates.
4. Calculate each flatmate's share.
5. Generate a PDF report.
6. Optionally upload the report and generate a shareable link.

## Learning Objectives

This project was created to practice:

- Object-Oriented Programming
- Class Design
- Object Collaboration
- PDF Generation
- Command Line Applications
- Real-world Problem Modeling

## Environment Setup

This project is part of a larger Python learning repository.

Dependencies are managed at the repository level using:

- `pyproject.toml`
- `uv.lock`

From the repository root:

```bash
uv sync
```

Run the application:

```bash
python main.py
```