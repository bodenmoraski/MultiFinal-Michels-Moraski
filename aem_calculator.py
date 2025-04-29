from typing import Dict, Any, Tuple
import math
import numpy as np
from scipy.stats import entropy

class AEMCalculator:
    def __init__(self):
        """Initialize the AEM calculator with advanced mathematical modeling."""
        # Base weights that will be adjusted by entropy
        self.base_weights = {
            'program_expense_ratio': 0.3,
            'fundraising_efficiency': 0.2,
            'revenue_sustainability': 0.15,
            'net_surplus_margin': 0.15,
            'executive_pay_reasonableness': 0.1,
            'transparency': 0.1
        }
        
        # Constants for sigmoid normalization
        self.sigmoid_shift = 0.5
        self.sigmoid_scale = 10
        
        # Fuzzy logic parameters for policy evaluation
        self.policy_weights = {
            'conflict_of_interest_policy': 0.3,
            'whistleblower_policy': 0.3,
            'document_retention_policy': 0.2,
            'compensation_review_process': 0.2
        }

    def _multi_dimensional_normalization(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Apply multi-dimensional normalization using Mahalanobis distance principles."""
        # Convert metrics to numpy array
        values = np.array(list(metrics.values()))
        
        # Calculate mean and standard deviation
        mean = np.mean(values)
        std = np.std(values)
        
        # Apply z-score normalization
        z_scores = (values - mean) / std
        
        # Convert back to sigmoid space
        normalized = {}
        for metric, z_score in zip(metrics.keys(), z_scores):
            normalized[metric] = self._sigmoid_normalization(z_score)
            
        return normalized

    def _calculate_entropy_weights(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate weights based on Shannon entropy of each metric."""
        # Convert metrics to probabilities
        total = sum(metrics.values())
        probabilities = [v/total for v in metrics.values()]
        
        # Calculate entropy for each metric
        entropies = {}
        for metric, value in metrics.items():
            # Create a binary distribution for the metric
            p = value/total
            dist = [p, 1-p]
            entropies[metric] = entropy(dist)
        
        # Normalize entropies to get weights
        total_entropy = sum(entropies.values())
        weights = {metric: e/total_entropy for metric, e in entropies.items()}
        
        return weights

    def _fuzzy_policy_evaluation(self, policies: Dict[str, bool]) -> float:
        """Evaluate policies using fuzzy logic."""
        if not policies:
            return 0.0
            
        # Calculate weighted sum of policies
        score = sum(
            weight * (1.0 if policy else 0.0)
            for policy, weight in zip(policies.values(), self.policy_weights.values())
        )
        
        # Apply sigmoid to get smooth transition
        return self._sigmoid_normalization(score)

    def calculate_aem(self, financials: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        """Calculate the Altruistic Effectiveness Metric (AEM) score with component scores."""
        # Calculate raw metrics
        raw_metrics = {
            'program_expense_ratio': self._calculate_program_expense_ratio(financials),
            'fundraising_efficiency': self._calculate_fundraising_efficiency(financials),
            'revenue_sustainability': self._calculate_revenue_sustainability(financials),
            'net_surplus_margin': self._calculate_net_surplus_margin(financials),
            'executive_pay_reasonableness': self._calculate_executive_pay_reasonableness(financials),
            'transparency': self._fuzzy_policy_evaluation(financials.get('policies', {}))
        }
        
        # Calculate entropy-based weights
        entropy_weights = self._calculate_entropy_weights(raw_metrics)
        
        # Apply multi-dimensional normalization
        normalized_metrics = self._multi_dimensional_normalization(raw_metrics)
        
        # Calculate final weights by combining base weights and entropy weights
        final_weights = {
            metric: (self.base_weights[metric] + entropy_weights[metric]) / 2
            for metric in self.base_weights
        }
        
        # Normalize final weights
        total_weight = sum(final_weights.values())
        final_weights = {metric: weight/total_weight for metric, weight in final_weights.items()}
        
        # Calculate weighted sum
        aem_score = sum(
            weight * score
            for weight, score in zip(final_weights.values(), normalized_metrics.values())
        )
        
        return aem_score, normalized_metrics

    def _calculate_program_expense_ratio(self, financials: Dict[str, Any]) -> float:
        """Calculate the ratio of program expenses to total expenses."""
        if 'largest_program_expenses' not in financials:
            return 0.0
        
        total_program_expenses = sum(
            program.get('expenses', 0)
            for program in financials['largest_program_expenses'].values()
        )
        return total_program_expenses / financials['total_expenses']

    def _calculate_fundraising_efficiency(self, financials: Dict[str, Any]) -> float:
        """Calculate and normalize fundraising efficiency."""
        if financials['fundraising_expenses'] == 0:
            return 0.0
        
        efficiency = financials['contributions_and_grants'] / financials['fundraising_expenses']
        return math.log10(efficiency + 1)  # Log scale for better distribution

    def _calculate_revenue_sustainability(self, financials: Dict[str, Any]) -> float:
        """Calculate the ratio of program service revenue to total revenue."""
        if financials['total_revenue'] == 0:
            return 0.0
        return financials['program_service_revenue'] / financials['total_revenue']

    def _calculate_net_surplus_margin(self, financials: Dict[str, Any]) -> float:
        """Calculate the net surplus margin."""
        if financials['total_revenue'] == 0:
            return 0.0
        return (financials['total_revenue'] - financials['total_expenses']) / financials['total_revenue']

    def _calculate_executive_pay_reasonableness(self, financials: Dict[str, Any]) -> float:
        """Calculate the reasonableness of executive pay using advanced statistical methods."""
        if not financials.get('top_individual_salaries') or financials['total_expenses'] == 0:
            return 1.0
        
        top_salary = max(financials['top_individual_salaries'].values())
        total_expenses = financials['total_expenses']
        
        # Calculate ratio and apply exponential decay
        ratio = top_salary / total_expenses
        return math.exp(-10 * ratio)  # Exponential decay for high ratios

    def _sigmoid_normalization(self, x: float) -> float:
        """Apply sigmoid normalization to a value."""
        return 1 / (1 + math.exp(-self.sigmoid_scale * (x - self.sigmoid_shift))) 