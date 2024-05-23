import numpy as np
import matplotlib.pyplot as plt

class AHP:
    def __init__(self, criteria):
        self.criteria = criteria
        self.alternatives = []
        self.criteria_weights = None
        self.alternatives_scores = None

    def get_alternatives(self):
        while True:
            try:
                num_alternatives = int(input("Enter the number of alternatives: "))
                if num_alternatives <= 0:
                    print("Please enter a positive integer.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer.")

        for i in range(num_alternatives):
            alternative_name = input(f"Enter the name of alternative {i + 1}: ")
            self.alternatives.append(alternative_name)

    def get_input(self):
        # Input for criteria weights
        criteria_weights = {}
        for criterion in self.criteria:
            while True:
                try:
                    weight = float(input(f"Enter the weight for the criterion '{criterion}': "))
                    if not 0 <= weight <= 10:
                        print("Please enter a value between 0 and 10.")
                    else:
                        criteria_weights[criterion] = weight
                        break
                except ValueError:
                    print("Please enter a valid number.")

        self.criteria_weights = criteria_weights

        # Input for alternatives scores
        alternatives_scores = {}
        for alternative in self.alternatives:
            scores = {}
            print(f"Enter scores for alternative '{alternative}':")
            for criterion in self.criteria:
                while True:
                    try:
                        score = float(input(f"Score for criterion '{criterion}': "))
                        if not 0 <= score <= 10:
                            print("Please enter a value between 0 and 10.")
                        else:
                            scores[criterion] = score
                            break
                    except ValueError:
                        print("Please enter a valid number.")
            alternatives_scores[alternative] = scores
        self.alternatives_scores = alternatives_scores

    def calculate_weights(self):
        # Construct the criteria pairwise comparison matrix
        criteria_matrix = np.zeros((len(self.criteria), len(self.criteria)))
        for i, criterion1 in enumerate(self.criteria):
            for j, criterion2 in enumerate(self.criteria):
                if i == j:
                    criteria_matrix[i, j] = 1
                elif i < j:
                    while True:
                        try:
                            comparison = float(input(f"How much more important is '{criterion1}' than '{criterion2}' (scale 1-9)?: "))
                            if not 1 <= comparison <= 9:
                                print("Please enter a value between 1 and 9.")
                            else:
                                criteria_matrix[i, j] = comparison
                                break
                        except ValueError:
                            print("Please enter a valid number.")
                else:
                    criteria_matrix[i, j] = 1 / criteria_matrix[j, i]
        
        # Calculate criteria weights using geometric mean method
        criteria_weights = np.prod(criteria_matrix, axis=1) ** (1 / len(self.criteria))
        criteria_weights /= np.sum(criteria_weights)
        self.criteria_weights = dict(zip(self.criteria, criteria_weights))

    def calculate_alternatives_scores(self):
        # Calculate the weighted scores for each alternative
        alternatives_scores = {}
        for alternative, scores in self.alternatives_scores.items():
            weighted_scores = np.zeros(len(self.criteria))
            for i, criterion in enumerate(self.criteria):
                weighted_scores[i] = scores[criterion] * self.criteria_weights[criterion]
            alternatives_scores[alternative] = np.sum(weighted_scores)
        self.alternatives_scores = alternatives_scores

    def rank_alternatives(self):
        # Rank alternatives based on their scores
        sorted_alternatives = sorted(self.alternatives_scores.items(), key=lambda x: x[1], reverse=True)
        print("\nAlternatives Ranking:")
        for rank, (alternative, score) in enumerate(sorted_alternatives, start=1):
            print(f"{rank}. {alternative}: {score:.4f}")

    def plot_alternatives_scores(self):
        # Plot alternatives scores using a horizontal bar chart
        alternatives = list(self.alternatives_scores.keys())
        scores = list(self.alternatives_scores.values())
        plt.figure(figsize=(10, 6))
        plt.barh(alternatives, scores, color='skyblue')
        plt.xlabel('Score')
        plt.title('Alternatives Scores')
        plt.gca().invert_yaxis()
        plt.show()

# Define the criteria
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

# Initialize AHP with the defined criteria
ahp = AHP(criteria)
ahp.get_alternatives()         # Ask user for the alternatives
ahp.get_input()                # Get user input for weights and scores
ahp.calculate_weights()        # Calculate weights for criteria
ahp.calculate_alternatives_scores() # Calculate scores for alternatives
ahp.rank_alternatives()        # Rank the alternatives
ahp.plot_alternatives_scores() # Plot the alternatives scores