def calculate_bonus(salary, rate=0.1, *extras, **options):
    bonus = salary * rate + sum(extras)

    if "cap" in options:
        bonus = min(bonus, options["cap"])

    return bonus


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def get_details(self):
        return f"{self.name} - {self.salary}"

    @property
    def annual_salary(self):
        return self.salary * 12


def log_call(func):
    def wrapper(*args, **kwargs):
        print("Calling get_details")
        return func(*args, **kwargs)

    return wrapper


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

        @log_call
        def get_details(self):
            return f"{self.name} - {self.salary} - Team Size: {self.team_size}"


employees = [
    {"name": "Arun", "department": "Sales", "salary": 30000},
    {"name": "Priya", "department": "HR", "salary": 45000},
    {"name": "Rahul", "department": "IT", "salary": 60000},
    {"name": "Divya", "department": "IT", "salary": 75000},
    {"name": "Karthik", "department": "Finance", "salary": 90000},
]


for emp in employees:
    salary = emp["salary"]

    if salary < 50000:
        category = "Low Salary"
    elif salary < 70000:
        category = "Medium Salary"
    else:
        category = "High Salary"

    print(f"{emp['name']} - {category}")


bonus = calculate_bonus(75000, 0.1, 1000, 2000, cap=8000)

manager = Manager("Divya", 75000, 5)

print(manager.get_details())
print("Annual Salary:", manager.annual_salary)
