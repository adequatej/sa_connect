majors = ["CS", "DS", "MA", "ME", "RBE"]

departments = ["Computer Science", "Data Science", "Mathematics", "Mechanical Engineering", "Robotics Engineering"]

courses = [{'major':'CS','coursenum':'1101'},
          {'major':'DS','coursenum':'4432'},
          {'major':'RBE','coursenum':'2010'},
          {'major':'ME','coursenum':'2221'}, 
          {'major':'MA','coursenum': '3031'},
          {'major':'CS','coursenum':'2303'},
          {'major':'CS','coursenum':'3733'},
          {'major':'CS','coursenum':'3013'},
          {'major':'DS','coursenum':'4441'}, 
          {'major':'MA','coursenum': '1024'}  ]

grad_years = [2024, 2025, 2026, 2027, 2028, 2029, 2030]
class_years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
terms = ["A", "B", "C", "D", "E1", "E2"]

past_class_terms = []
for y in class_years:
    for t in terms:
        past_class_terms.append(f"{y}-{t}")

future_class_terms = []
for y in grad_years:
    for t in terms:
        future_class_terms.append(f"{y}-{t}")

grades = ["A", "B", "C"]

min_grades = grades.copy()
min_grades.append("None")