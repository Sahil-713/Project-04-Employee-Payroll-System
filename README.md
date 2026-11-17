# 💼 Project 04 – Employee Payroll System

## 📌 Overview

The Employee Payroll System is a Python-based console application developed using Object-Oriented Programming (OOP) concepts. It is designed to manage employee information, calculate salaries, maintain payroll records, and generate individual employee payslips.

The application supports two types of employees: Full-time Employees and Contract Employees. It provides a menu-driven interface that allows users to add employees, display employee records, search for employees, calculate salaries, and generate payslips.

Employee information and payroll records are stored using CSV file handling, ensuring that important records remain available between program executions.

## 🚀 Features

- **Add Employee:** Register new employees with a unique employee ID, name, and department.
- **Full-time Employee:** Store basic salary, allowances, and deductions.
- **Contract Employee:** Calculate salary using hourly rates and hours worked.
- **Display Employees:** View all registered employees with their details and net salaries.
- **Search Employee:** Find employee records using their unique employee ID.
- **Salary Calculation:** Calculate gross salary, deductions, and net salary.
- **Generate Payslip:** Create individual employee payslips in text format.
- **CSV File Handling:** Automatically save and load employee information.
- **Payroll Records:** Store calculated salary details with transaction dates.
- **Input Validation:** Handle invalid numeric inputs, negative values, and duplicate employee IDs.
- **Exception Handling:** Handle file-related errors and invalid operations.

## 🛠️ Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- CSV Module
- OS Module
- Datetime Module
- Abstract Base Classes
- Exception Handling
- File Handling

## 🧠 OOP Concepts Implemented

**1. Abstraction**

The `Employee` class is an abstract base class that defines common employee information and abstract methods for salary calculation and employee type identification.

**2. Inheritance**

The `FullTimeEmployee` and `ContractEmployee` classes inherit from the `Employee` base class and implement their own salary calculation methods.

**3. Encapsulation**

Private attributes are used to protect employee information, including employee ID, name, department, salary details, and deductions. Getter and setter methods provide controlled access.

**4. Polymorphism**

Both employee subclasses implement their own `calculate_gross_salary()` method, allowing salary calculations to work according to the employee type.

**5. Classes and Objects**

The project uses separate classes to organize employee information and payroll management operations.

## 💰 Salary Calculation

The system calculates salaries using the following formulas:

**Full-time Employee**

```text
Gross Salary = Basic Salary + Allowances

Net Salary = Gross Salary - Deductions
```

**Contract Employee**

```text
Gross Salary = Hourly Rate × Hours Worked

Net Salary = Gross Salary - Deductions
```

The system does not allow the calculated net salary to fall below zero.

## 📂 Project Structure

```text
Project-04-Employee-Payroll-System/
│
├── Screenshots/
│
├── payslips/
│
├── Employee Payroll System.py
├── employees.csv
├── payroll_records.csv
└── README.md
```

**File Description:**

| File / Folder | Purpose |
|---|---|
| Screenshots | Contains project execution screenshots |
| payslips | Stores generated employee payslips |
| Employee Payroll System.py | Main Python application |
| employees.csv | Stores employee information |
| payroll_records.csv | Stores calculated payroll records |
| README.md | Project documentation |

*Note: CSV files and the payslips folder are generated automatically when the application performs the corresponding operations.*

## 💻 Application Menu

```text
=============================================
       EMPLOYEE PAYROLL SYSTEM
=============================================
1. Add Employee
2. Display All Employees
3. Search Employee
4. Calculate Salary / Save Payroll
5. Generate Payslip
6. Exit
=============================================
```

## ⚙️ How to Run the Project

**Step 1:** Install Python 3 on your computer.

**Step 2:** Clone the repository:

```bash
git clone https://github.com/Sahil-713/Project-04-Employee-Payroll-System.git
```

**Step 3:** Navigate to the project directory:

```bash
cd Project-04-Employee-Payroll-System
```

**Step 4:** Run the Python application:

```bash
python "Employee Payroll System.py"
```

No external Python libraries are required.

## 📄 Payslip Generation

The application generates individual employee payslips in `.txt` format.

Each payslip includes:

- Employee ID
- Employee name
- Department
- Employee type
- Basic salary and allowances or hourly rate and hours worked
- Gross salary
- Deductions
- Net salary
- Payslip generation date and time

Generated payslips are stored inside the `payslips` folder.

## 📁 Data Storage

The application uses CSV files to maintain employee and payroll information.

- `employees.csv` stores employee details and salary information.
- `payroll_records.csv` stores salary calculations, deductions, and net salary.
- Individual payslips are saved as text files inside the `payslips` folder.

## 📚 Learning Outcomes

Through this project, I practised:

- Implementing abstraction, inheritance, encapsulation, and polymorphism.
- Designing classes and objects in Python.
- Using abstract base classes and method overriding.
- Implementing salary calculation logic.
- Reading and writing CSV files.
- Generating formatted payslips.
- Applying input validation and exception handling.
- Developing a menu-driven console application.

## 👨‍💻 Author

**Sahil Singh**

GitHub: [Sahil-713](https://github.com/Sahil-713)

**Repository:** [Project 04 – Employee Payroll System](https://github.com/Sahil-713/Project-04-Employee-Payroll-System)

---

*Developed as part of Python programming and Object-Oriented Programming practice.*
