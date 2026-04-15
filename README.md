1. Короткий опис проєкту та релевантність задачі
Проєкт реалізує систему підтримки прийняття рішень для вибору оптимальної платформи кіберзахисту.
Релевантність: Задача є напівструктурованою, оскільки вибір базується як на жорстких метриках (вартість, % виявлення вірусів), так і на суб’єктивних чинниках (якість підтримки, репутація).
Необхідність СППР: Кількість факторів та альтернатив перевищує можливості людини для об’єктивного аналізу без математичних моделей, особливо в умовах обмеженого бюджету та високих ризиків.
2. Формалізація задачі
Множина альтернатив (A): А = А1 - Vendor A (Enterprise), A2 - Vendor B (Cloud), A3 - Vendor C (Open-Source).
Множина критеріїв (C):
C1: Ефективність (Max) — якість виявлення атак.
C2: Вартість (Min) — сукупні витрати.
C3: Сумісність (Max) — інтеграція з PostgreSQL/DBeaver.
C4: Продуктивність (Min) — навантаження на систему.
C5: Підтримка (Max) — якість SLA.
3. Архітектура системи
Система реалізована на мові Python із чітким розділенням на шари (Controller / Service / Data), що забезпечує читабельність та можливість розширення:
Data Layer: Сутності Alternative, Criterion, Evaluation та SQL-схема.
Service Layer (Core): Аналітичне ядро, що реалізує методи SAW (Зважена сума) та Відстань до ідеалу.
Controller (CLI/API): Забезпечує ввід даних та вивід результатів.
4. Схема бази даних (SQL)
Використовується реляційна структура для збереження матриці оцінювання.
CREATE TABLE alternatives (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE criteria (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(10) CHECK (type IN ('maximize', 'minimize')),
    weight NUMERIC(3, 2)
);

CREATE TABLE evaluations (
    alt_id INT REFERENCES alternatives(id),
    crit_id INT REFERENCES criteria(id),
    score NUMERIC(5, 2),
    PRIMARY KEY (alt_id, crit_id)
);

5. Програмна реалізація (Python)
import math

class DSSData:
    def __init__(self):
        self.alternatives = {}
        self.criteria = {}
        self.matrix = {} # {(alt_id, crit_id): score}

class DSSService:
    def __init__(self, data):
        self.data = data

    def calculate_saw(self):
        """Метод зваженої суми (SAW)"""
        results = {}
        for a_id, a_name in self.data.alternatives.items():
            score = 0
            for c_id, c_info in self.data.criteria.items():
                val = self.data.matrix.get((a_id, c_id), 0)
                actual_val = val if c_info['type'] == 'maximize' else (11 - val)
                score += actual_val * c_info['weight']
            results[a_name] = round(score, 2)
        return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

    def calculate_ideal_dist(self):
        """Метод відстані до ідеальної точки (менше = краще)"""
        results = {}
        for a_id, a_name in self.data.alternatives.items():
            dist_sq = 0
            for c_id, c_info in self.data.criteria.items():
                val = self.data.matrix.get((a_id, c_id), 0)
                ideal = 10 if c_info['type'] == 'maximize' else 1
                dist_sq += c_info['weight'] * (ideal - val)**2
            results[a_name] = round(math.sqrt(dist_sq), 2)
        return dict(sorted(results.items(), key=lambda x: x[1]))

class DSSController:
    def __init__(self):
        self.db = DSSData()
        self.service = DSSService(self.db)

    def seed_data(self):
        self.db.alternatives = {1: "Vendor A (Enterprise)", 2: "Vendor B (Cloud)", 3: "Vendor C (Open Source)"}
        self.db.criteria = {
            1: {'name': 'Ефективність', 'type': 'maximize', 'weight': 0.35},
            2: {'name': 'Вартість', 'type': 'minimize', 'weight': 0.25},
            3: {'name': 'Сумісність', 'type': 'maximize', 'weight': 0.20},
            4: {'name': 'Продуктивність', 'type': 'minimize', 'weight': 0.10},
            5: {'name': 'Підтримка', 'type': 'maximize', 'weight': 0.10}
        }
        self.db.matrix = {
            (1,1): 10, (1,2): 8, (1,3): 7, (1,4): 5, (1,5): 9, # Vendor A
            (2,1): 8,  (2,2): 5, (2,3): 8, (2,4): 3, (2,5): 7, # Vendor B
            (3,1): 6,  (3,2): 2, (3,3): 10, (3,4): 2, (3,5): 4  # Vendor C
        }

    def run(self):
        self.seed_data()
        print("--- РЕЗУЛЬТАТИ СППР (Метод SAW) ---")
        print(self.service.calculate_saw())
        print("\n--- РЕЗУЛЬТАТИ СППР (Відстань до ідеалу) ---")
        print(self.service.calculate_ideal_dist())

if __name__ == "__main__":
    app = DSSController()
    app.run()

6. Результат роботи та пояснення рішення
Система проводить інтегральне оцінювання за двома стратегіями.
Ранжування: Вибудовує список від найкращої до найгіршої альтернативи. Найкращою альтернативою зазвичай стає Vendor B, оскільки він збалансований. Vendor A надто дорогий, а Vendor C має критично низьку підтримку.
Логіка базується на зважуванні — кожен бал множиться на важливість (вагу) критерію, що дозволяє об’єктивно порівняти непорівнювані речі (гроші та безпеку).
