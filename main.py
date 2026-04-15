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