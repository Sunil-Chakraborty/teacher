
from django.core.management.base import BaseCommand

#python manage.py linear_examp

from sklearn.datasets import make_classification, make_circles
import matplotlib.pyplot as plt

class Command(BaseCommand):

    help = "Linear Example"

    def handle(self, *args, **options):
        # Fix: Ensure the sum constraint
        X, y = make_classification(
            n_samples=100, 
            n_features=4,          # Total features
            n_informative=2,       # Informative features
            n_redundant=1,         # Redundant features
            n_repeated=0,          # Repeated features
            n_classes=2, 
            random_state=42
        )

        # Visualize the dataset
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm')
        plt.title("Linearly Separable Data")
        plt.show()

    def handle(self, *args, **options):
        X, y = make_circles(n_samples=100, noise=0.1, factor=0.5, random_state=42)
        plt.scatter(X[:, 0], X[:, 1], c=y, cmap='coolwarm')
        plt.title("Non-Linearly Separable Data")
        plt.show()
