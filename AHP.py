import numpy as np

class AHP:
    def __init__(self, criteria, alternatives):
        self.criteria = criteria
        self.alternatives = alternatives
        self.criteria_weights = None
        self.alternatives_scores = None

    def get_input(self):
        criteria_weights = {}
        for criterion in self.criteria:
            weight = float(input(f"Enter the weight for the criterion '{criterion}': "))
            criteria_weights[criterion] = weight
        self.criteria_weights = criteria_weights

        alternatives_scores = {}
        for alternative in self.alternatives:
            scores = {}
            print(f"Enter scores for alternative '{alternative}':")
            for criterion in self.criteria:
                score = float(input(f"Score for criterion '{criterion}': "))
                scores[criterion] = score
            alternatives_scores[alternative] = scores
        self.alternatives_scores = alternatives_scores

    def calculate_weights(self):
        criteria_matrix = np.zeros((len(self.criteria), len(self.criteria)))
        for i, criterion1 in enumerate(self.criteria):
            for j, criterion2 in enumerate(self.criteria):
                if i == j:
                    criteria_matrix[i, j] = 1
                elif i < j:
                    criteria_matrix[i, j] = float(input(f"How much more important is '{criterion1}' than '{criterion2}'?: "))
                else:
                    criteria_matrix[i, j] = 1 / criteria_matrix[j, i]
        criteria_weights = np.prod(criteria_matrix, axis=1) ** (1 / len(self.criteria))
        criteria_weights /= np.sum(criteria_weights)
        self.criteria_weights = dict(zip(self.criteria, criteria_weights))

    def calculate_alternatives_scores(self):
        alternatives_scores = {}
        for alternative, scores in self.alternatives_scores.items():
            weighted_scores = np.zeros(len(self.criteria))
            for i, criterion in enumerate(self.criteria):
                weighted_scores[i] = scores[criterion] * self.criteria_weights[criterion]
            alternatives_scores[alternative] = np.sum(weighted_scores)
        self.alternatives_scores = alternatives_scores

    def rank_alternatives(self):
        sorted_alternatives = sorted(self.alternatives_scores.items(), key=lambda x: x[1], reverse=True)
        print("\nAlternatives Ranking:")
        for rank, (alternative, score) in enumerate(sorted_alternatives, start=1):
            print(f"{rank}. {alternative}: {score}")

criteria = [
    "Air Quality", 
    "Water Quality", 
    "Soil Quality and Land Use", 
    "Waste Management", 
    "Energy Efficiency", 
    "Resilience to Natural Disasters", 
    "Biodiversity and Green Areas", 
    "Sustainable Mobility", 
    "Urban Safety", 
    "Equity and Social Justice", 
    "Citizen Participation and Urban Governance", 
    "Economic Impact and Employment", 
    "Access to Public Services and Amenities"
]

alternatives = ["Plan A", "Plan B", "Plan C"]

ahp = AHP(criteria, alternatives)
ahp.get_input()
ahp.calculate_weights()
ahp.calculate_alternatives_scores()
ahp.rank_alternatives()
