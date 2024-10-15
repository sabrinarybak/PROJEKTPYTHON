import json #använder inbydda biblioteket json för att spara och ladda upp uppgifter/tasks

#Tre klasser - Task, Category och User

#Klass för en uppgift
class Task: #representerar en uppgift med titel, prio(Hög,Medel,Låg) och status(klar/ej klar)
    def __init__(self, title, priority, is_completed=False):
        self.title = title
        self.priority = priority #Hög, Medel, Låg
        self.is_completed = is_completed

    def complete_task(self):
        self.is_completed = True

# Klass för en kategori som innehåller flera uppgifter
class Category:
    def __init__(self, name):
        self.name = name
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def incomplete_tasks(self):
        return [task for task in self.tasks if not task.is_completed]
    
    def complete_tasks(self):
        return [task for task in self.tasks if task.is_completed]
    
#Klass för användaren som har flera kategorier och uppgifter
class User:
    def __init__(self, name):
        self.name = name
        self.categories = []

    def add_category(self, category):
        self.categories.append(category)
    
    def save_tasks(self, filename):
        data = []
        for category in self.categories:
            category_data = {
                'name':category.name,
                'tasks': [{'title': task.title, 'priority': task.priority, 'is_completed': task.is_completed} for task in category.tasks]
            }
            data.append(category_data)
        with open('tasks.json','w') as file:
            json.dump(data, file, indent=4)
        
    def load_tasks(self, filename):
        try:
            with open(filename, 'r') as file:
                categories_data = json.load(file)
                for category_data in categories_data:
                    category = Category(category_data['name'])
                    for task_data in category_data['tasks']:
                        task = Task(task_data['title'], task_data['priority'], task_data['is_completed'])

                        category.add_task(task)
                    self.categories.append(category)
        except FileNotFoundError:
            print(f"Filen {filename} kunde inte hittas.")

#skapa några uppgifter
task1 = Task('Handla hundmat', 'High')
task2 = Task('Dammsuga vardagsrummet','Medium')
task3 = Task('Handla nya bestick', 'Low')

#skapa en kategori och lägg till uppgifterna
category1 = Category('Hemmasysslor')
category1.add_task(task1)
category1.add_task(task2)
category1.add_task(task3)

#skapa en användare och lägg till i kategorin
user = User('Bob')
user.add_category(category1)

#spara uppgifterna till en fil

user.save_tasks('tasks.json')

#visa ofullständiga uppgifter
incomplete = category1.incomplete_tasks()
print("Du är inte klar med:")
for task in incomplete:
    print(f"- {task.title} (Prioritet: {task.priority})")

#slutför en uppgift och visa de som är slutförda
task1.complete_task()
completed = category1.complete_tasks()
print("\nYay! Du är klar med:")
for task in completed:
     print(f"-{task.title} (Prioritet: {task.priority})")

#slutför en uppgift från filen
user.load_tasks('tasks.json')

#fråga användaren om de vill lägga till en ny uppgift
while True:
    title = input("Skriv din uppgift (eller skriv 'klar' för att avsluta:)")
    if title.lower() == 'klar':
        break
    priority = input ("Ange prioritet (High, Medium, Low):")

    #skapa en ny uppgift och lägg till den i en kategori
    new_task = Task(title, priority)

user.categories[0].add_task(new_task)
#tet
#spara de uppdaterade uppgifterna till filen igen
user.save_tasks('tasks.json')
