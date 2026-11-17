import csv
import os
from abc import ABC, abstractmethod
from datetime import datetime

EMPLOYEE_FILE = "employees.csv"
PAYROLL_FILE = "payroll_records.csv"
PAYSLIP_DIR = "payslips"


# ==============================
# Abstract Base Class
# ==============================
class Employee(ABC):

    def __init__(self, employee_id, name, department, deductions=0):
        self.__employee_id = employee_id
        self.__name = name
        self.__department = department
        self.__deductions = float(deductions)

    # Getters
    def get_employee_id(self):
        return self.__employee_id

    def get_name(self):
        return self.__name

    def get_department(self):
        return self.__department

    def get_deductions(self):
        return self.__deductions

    # Setters
    def set_name(self, name):
        if not name.strip():
            raise ValueError("Employee name cannot be empty.")
        self.__name = name.strip()

    def set_department(self, department):
        if not department.strip():
            raise ValueError("Department cannot be empty.")
        self.__department = department.strip()

    def set_deductions(self, deductions):
        deductions = float(deductions)
        if deductions < 0:
            raise ValueError("Deductions cannot be negative.")
        self.__deductions = deductions

    @abstractmethod
    def calculate_gross_salary(self):
        pass

    @abstractmethod
    def get_employee_type(self):
        pass

    @abstractmethod
    def to_csv_row(self):
        pass

    def calculate_net_salary(self):
        net_salary = self.calculate_gross_salary() - self.__deductions
        return max(0, net_salary)


# ==============================
# Full-Time Employee Class
# ==============================
class FullTimeEmployee(Employee):

    def __init__(
        self, employee_id, name, department, basic_salary, allowances=0, deductions=0
    ):

        super().__init__(employee_id, name, department, deductions)

        self.__basic_salary = float(basic_salary)
        self.__allowances = float(allowances)

        if self.__basic_salary < 0 or self.__allowances < 0:
            raise ValueError("Salary and allowances cannot be negative.")

    def get_basic_salary(self):
        return self.__basic_salary

    def set_basic_salary(self, amount):
        amount = float(amount)
        if amount < 0:
            raise ValueError("Basic salary cannot be negative.")
        self.__basic_salary = amount

    def get_allowances(self):
        return self.__allowances

    def set_allowances(self, amount):
        amount = float(amount)
        if amount < 0:
            raise ValueError("Allowances cannot be negative.")
        self.__allowances = amount

    def calculate_gross_salary(self):
        return self.__basic_salary + self.__allowances

    def get_employee_type(self):
        return "Full-time"

    def to_csv_row(self):
        return {
            "employee_id": self.get_employee_id(),
            "name": self.get_name(),
            "department": self.get_department(),
            "employee_type": self.get_employee_type(),
            "basic_salary": self.__basic_salary,
            "allowances": self.__allowances,
            "hourly_rate": "",
            "hours_worked": "",
            "deductions": self.get_deductions(),
        }


# ==============================
# Contract Employee Class
# ==============================
class ContractEmployee(Employee):

    def __init__(
        self, employee_id, name, department, hourly_rate, hours_worked, deductions=0
    ):

        super().__init__(employee_id, name, department, deductions)

        self.__hourly_rate = float(hourly_rate)
        self.__hours_worked = float(hours_worked)

        if self.__hourly_rate < 0 or self.__hours_worked < 0:
            raise ValueError("Hourly rate and hours cannot be negative.")

    def get_hourly_rate(self):
        return self.__hourly_rate

    def set_hourly_rate(self, amount):
        amount = float(amount)
        if amount < 0:
            raise ValueError("Hourly rate cannot be negative.")
        self.__hourly_rate = amount

    def get_hours_worked(self):
        return self.__hours_worked

    def set_hours_worked(self, hours):
        hours = float(hours)
        if hours < 0:
            raise ValueError("Hours worked cannot be negative.")
        self.__hours_worked = hours

    def calculate_gross_salary(self):
        return self.__hourly_rate * self.__hours_worked

    def get_employee_type(self):
        return "Contract"

    def to_csv_row(self):
        return {
            "employee_id": self.get_employee_id(),
            "name": self.get_name(),
            "department": self.get_department(),
            "employee_type": self.get_employee_type(),
            "basic_salary": "",
            "allowances": "",
            "hourly_rate": self.__hourly_rate,
            "hours_worked": self.__hours_worked,
            "deductions": self.get_deductions(),
        }


# ==============================
# Payroll Management Class
# ==============================
class PayrollSystem:

    FIELDNAMES = [
        "employee_id",
        "name",
        "department",
        "employee_type",
        "basic_salary",
        "allowances",
        "hourly_rate",
        "hours_worked",
        "deductions",
    ]

    def __init__(self):
        self.__employees = []
        self.load_employees()

    def get_employees(self):
        return self.__employees.copy()

    # Find employee using ID
    def find_employee(self, employee_id):
        for employee in self.__employees:
            if employee.get_employee_id().lower() == employee_id.lower():
                return employee
        return None

    # Add a new employee
    def add_employee(self, employee):
        if self.find_employee(employee.get_employee_id()):
            raise ValueError("An employee with this ID already exists.")

        self.__employees.append(employee)
        self.save_employees()

    # Load employee records from CSV
    def load_employees(self):
        if not os.path.exists(EMPLOYEE_FILE):
            return

        try:
            with open(EMPLOYEE_FILE, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    employee_type = row["employee_type"]

                    if employee_type == "Full-time":
                        employee = FullTimeEmployee(
                            row["employee_id"],
                            row["name"],
                            row["department"],
                            float(row["basic_salary"]),
                            float(row["allowances"]),
                            float(row["deductions"]),
                        )

                    elif employee_type == "Contract":
                        employee = ContractEmployee(
                            row["employee_id"],
                            row["name"],
                            row["department"],
                            float(row["hourly_rate"]),
                            float(row["hours_worked"]),
                            float(row["deductions"]),
                        )

                    else:
                        print("Unknown employee type. Record skipped.")
                        continue

                    if not self.find_employee(employee.get_employee_id()):
                        self.__employees.append(employee)

        except (OSError, csv.Error, ValueError, KeyError) as error:
            print("Could not load employee records:", error)

    # Save employee records to CSV
    def save_employees(self):
        try:
            with open(EMPLOYEE_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()

                for employee in self.__employees:
                    writer.writerow(employee.to_csv_row())

        except OSError as error:
            print("Error saving employee records:", error)

    # Search employee
    def search_employee(self, employee_id):
        return self.find_employee(employee_id)

    # Display all employees
    def display_employees(self):
        if not self.__employees:
            print("\nNo employee records found.")
            return

        print("\n" + "=" * 78)
        print(
            f"{'ID':<12}{'NAME':<22}{'DEPARTMENT':<18}"
            f"{'TYPE':<13}{'NET SALARY':>13}"
        )
        print("=" * 78)

        for employee in self.__employees:
            print(
                f"{employee.get_employee_id():<12}"
                f"{employee.get_name():<22}"
                f"{employee.get_department():<18}"
                f"{employee.get_employee_type():<13}"
                f"{employee.calculate_net_salary():>13.2f}"
            )

        print("=" * 78)

    # Generate employee payslip
    def generate_payslip(self, employee):

        os.makedirs(PAYSLIP_DIR, exist_ok=True)

        gross_salary = employee.calculate_gross_salary()
        deductions = employee.get_deductions()
        net_salary = employee.calculate_net_salary()

        # Prepare salary details
        if isinstance(employee, FullTimeEmployee):
            salary_details = [
                f"Basic Salary : Rs. {employee.get_basic_salary():,.2f}",
                f"Allowances   : Rs. {employee.get_allowances():,.2f}",
            ]
        else:
            salary_details = [
                f"Hourly Rate  : Rs. {employee.get_hourly_rate():,.2f}",
                f"Hours Worked : {employee.get_hours_worked():,.2f}",
            ]

        # Each payslip line is stored separately.
        # This prevents accidental repetition of the header.
        payslip_lines = [
            "=" * 45,
            "              EMPLOYEE PAYSLIP",
            "=" * 45,
            f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            f"Employee ID  : {employee.get_employee_id()}",
            f"Name         : {employee.get_name()}",
            f"Department   : {employee.get_department()}",
            f"Employee Type: {employee.get_employee_type()}",
            "-" * 45,
        ]

        payslip_lines.extend(salary_details)

        payslip_lines.extend(
            [
                "-" * 45,
                f"Gross Salary : Rs. {gross_salary:,.2f}",
                f"Deductions   : Rs. {deductions:,.2f}",
                f"Net Salary   : Rs. {net_salary:,.2f}",
                "=" * 45,
            ]
        )

        # Join all lines into one payslip string
        payslip = "\n".join(payslip_lines) + "\n"

        filename = os.path.join(
            PAYSLIP_DIR, f"{employee.get_employee_id()}_payslip.txt"
        )

        try:
            # "w" overwrites the previous payslip
            with open(filename, "w", encoding="utf-8") as file:
                file.write(payslip)

            print(f"\nPayslip generated: {filename}")

        except OSError as error:
            print("Error generating payslip:", error)

        return payslip

    # Save payroll calculation
    def save_payroll_record(self, employee):

        file_exists = os.path.exists(PAYROLL_FILE)

        fields = [
            "date",
            "employee_id",
            "name",
            "employee_type",
            "gross_salary",
            "deductions",
            "net_salary",
        ]

        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "employee_id": employee.get_employee_id(),
            "name": employee.get_name(),
            "employee_type": employee.get_employee_type(),
            "gross_salary": f"{employee.calculate_gross_salary():.2f}",
            "deductions": f"{employee.get_deductions():.2f}",
            "net_salary": f"{employee.calculate_net_salary():.2f}",
        }

        try:
            with open(PAYROLL_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fields)

                if not file_exists or os.path.getsize(PAYROLL_FILE) == 0:
                    writer.writeheader()

                writer.writerow(record)

            print("Payroll calculation saved successfully.")

        except OSError as error:
            print("Error saving payroll record:", error)


# ==============================
# Input Validation Functions
# ==============================
def get_non_empty_input(prompt):

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")


def get_non_negative_float(prompt):

    while True:
        try:
            value = float(input(prompt))

            if value < 0:
                print("Please enter zero or a positive number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# ==============================
# Add Employee Menu
# ==============================
def add_employee_menu(payroll):

    print("\n--- Add Employee ---")

    employee_id = get_non_empty_input("Enter employee ID: ")

    if payroll.search_employee(employee_id):
        print("An employee with this ID already exists.")
        return

    name = get_non_empty_input("Enter employee name: ")
    department = get_non_empty_input("Enter department: ")

    print("\n1. Full-time employee")
    print("2. Contract employee")

    employee_type = input("Choose employee type (1-2): ").strip()

    try:
        if employee_type == "1":

            basic_salary = get_non_negative_float("Enter basic salary (Rs.): ")
            allowances = get_non_negative_float("Enter allowances (Rs.): ")
            deductions = get_non_negative_float("Enter deductions (Rs.): ")

            employee = FullTimeEmployee(
                employee_id, name, department, basic_salary, allowances, deductions
            )

        elif employee_type == "2":

            hourly_rate = get_non_negative_float("Enter hourly rate (Rs.): ")
            hours_worked = get_non_negative_float("Enter hours worked: ")
            deductions = get_non_negative_float("Enter deductions (Rs.): ")

            employee = ContractEmployee(
                employee_id, name, department, hourly_rate, hours_worked, deductions
            )

        else:
            print("Invalid employee type.")
            return

        payroll.add_employee(employee)
        print("Employee added and saved successfully.")

    except ValueError as error:
        print("Could not add employee:", error)


# ==============================
# Search Employee Menu
# ==============================
def search_employee_menu(payroll):

    employee_id = input("Enter employee ID to search: ").strip()
    employee = payroll.search_employee(employee_id)

    if employee:
        print("\nEmployee found:")
        print("ID:", employee.get_employee_id())
        print("Name:", employee.get_name())
        print("Department:", employee.get_department())
        print("Type:", employee.get_employee_type())

        print(f"Gross salary: Rs. " f"{employee.calculate_gross_salary():,.2f}")
        print(f"Net salary: Rs. " f"{employee.calculate_net_salary():,.2f}")

    else:
        print("Employee not found.")


# ==============================
# Payroll Menu
# ==============================
def payroll_menu(payroll):

    employee_id = input("Enter employee ID for payroll: ").strip()
    employee = payroll.search_employee(employee_id)

    if not employee:
        print("Employee not found.")
        return

    print(f"\nEmployee: {employee.get_name()}")
    print(f"Gross salary: Rs. " f"{employee.calculate_gross_salary():,.2f}")
    print(f"Deductions: Rs. {employee.get_deductions():,.2f}")
    print(f"Net salary: Rs. " f"{employee.calculate_net_salary():,.2f}")

    payroll.save_payroll_record(employee)


# ==============================
# Payslip Menu
# ==============================
def payslip_menu(payroll):

    employee_id = input("Enter employee ID for payslip: ").strip()
    employee = payroll.search_employee(employee_id)

    if not employee:
        print("Employee not found.")
        return

    payroll.generate_payslip(employee)


# ==============================
# Main Function
# ==============================
def main():

    payroll = PayrollSystem()

    while True:

        print("\n" + "=" * 45)
        print("       EMPLOYEE PAYROLL SYSTEM")
        print("=" * 45)

        print("1. Add Employee")
        print("2. Display All Employees")
        print("3. Search Employee")
        print("4. Calculate Salary / Save Payroll")
        print("5. Generate Payslip")
        print("6. Exit")

        print("=" * 45)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_employee_menu(payroll)

        elif choice == "2":
            payroll.display_employees()

        elif choice == "3":
            search_employee_menu(payroll)

        elif choice == "4":
            payroll_menu(payroll)

        elif choice == "5":
            payslip_menu(payroll)

        elif choice == "6":
            payroll.save_employees()
            print("Employee records saved. Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please select between 1 and 6.")


# Start the program
if __name__ == "__main__":
    main()
