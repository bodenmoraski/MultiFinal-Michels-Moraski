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
        
        # Handle case where all values are the same
        if np.all(values == values[0]):
            return {metric: 0.5 for metric in metrics.keys()}
            
        # Calculate mean and standard deviation
        mean = np.mean(values)
        std = np.std(values)
        
        # Handle case where std is 0
        if std == 0:
            return {metric: 0.5 for metric in metrics.keys()}
            
        # Apply z-score normalization with clipping to prevent extreme values
        z_scores = np.clip((values - mean) / std, -3, 3)
        
        # Convert back to sigmoid space
        normalized = {}
        for metric, z_score in zip(metrics.keys(), z_scores):
            normalized[metric] = self._sigmoid_normalization(z_score)
            
        return normalized

    def _calculate_entropy_weights(self, metrics: Dict[str, float]) -> Dict[str, float]:
        """Calculate weights based on Shannon entropy of each metric."""
        # Add small constant to prevent zero values
        epsilon = 1e-10
        adjusted_metrics = {k: v + epsilon for k, v in metrics.items()}
        
        # Convert to probabilities
        total = sum(adjusted_metrics.values())
        probabilities = {k: v/total for k, v in adjusted_metrics.items()}
        
        # Calculate entropy for each metric
        entropies = {}
        for metric, prob in probabilities.items():
            # Create a binary distribution for the metric
            dist = [prob, 1-prob]
            entropies[metric] = entropy(dist)
        
        # Calculate inverse entropy weights (higher weight for lower entropy)
        max_entropy = max(entropies.values())
        inverse_entropies = {metric: (max_entropy - e + epsilon) 
                            for metric, e in entropies.items()}
        
        # Normalize inverse entropies to get weights
        total_inverse = sum(inverse_entropies.values())
        if total_inverse == 0:
            return self.base_weights
            
        weights = {metric: (inv_e + epsilon)/(total_inverse + len(entropies)*epsilon) 
                  for metric, inv_e in inverse_entropies.items()}
        
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
        # Use pre-calculated ratio if available
        if 'program_expense_ratio' in financials:
            ratio = financials['program_expense_ratio']
            # Normalize to 0-1 range with 0.6 as ideal
            return self._sigmoid_normalization(ratio - 0.6)
            
        if 'largest_program_expenses' not in financials or financials['total_expenses'] == 0:
            return 0.0
        
        total_program_expenses = sum(
            program.get('expenses', 0)
            for program in financials['largest_program_expenses'].values()
        )
        ratio = total_program_expenses / financials['total_expenses']
        # Normalize to 0-1 range with 0.6 as ideal
        return self._sigmoid_normalization(ratio - 0.6)

    def _calculate_fundraising_efficiency(self, financials: Dict[str, Any]) -> float:
        """Calculate and normalize fundraising efficiency."""
        # Use pre-calculated efficiency if available
        if 'fundraising_efficiency' in financials:
            efficiency = financials['fundraising_efficiency']
            # Normalize efficiency score (ideal around 10)
            # Use log scale to better handle high values
            return self._sigmoid_normalization(math.log10(efficiency) - 0.8)
            
        if financials['fundraising_expenses'] == 0:
            return 0.0
        
        efficiency = financials['contributions_and_grants'] / financials['fundraising_expenses']
        return self._sigmoid_normalization(math.log10(efficiency) - 0.8)

    def _calculate_revenue_sustainability(self, financials: Dict[str, Any]) -> float:
        """Calculate the ratio of program service revenue to total revenue."""
        if financials['total_revenue'] == 0:
            return 0.0
        ratio = financials['program_service_revenue'] / financials['total_revenue']
        # Normalize to 0-1 range with 0.5 as ideal
        return self._sigmoid_normalization(ratio - 0.5)

    def _calculate_net_surplus_margin(self, financials: Dict[str, Any]) -> float:
        """Calculate the net surplus margin."""
        if financials['total_revenue'] == 0:
            return 0.0
        margin = (financials['total_revenue'] - financials['total_expenses']) / financials['total_revenue']
        # Normalize margin to 0-1 range, with 0.05 (5%) as ideal
        return self._sigmoid_normalization(margin - 0.05)

    def _calculate_executive_pay_reasonableness(self, financials: Dict[str, Any]) -> float:
        """Calculate the reasonableness of executive pay using advanced statistical methods."""
        if not financials.get('top_individual_salaries') or financials['total_expenses'] == 0:
            return 0.5  # Neutral score if no data
        
        top_salary = max(financials['top_individual_salaries'].values())
        total_expenses = financials['total_expenses']
        
        # Calculate ratio and normalize
        ratio = top_salary / total_expenses
        # Ideal ratio is around 0.015 (1.5% of total expenses)
        return self._sigmoid_normalization(0.015 - ratio)

    def _sigmoid_normalization(self, x: float) -> float:
        """Apply sigmoid normalization to a value."""
        # Adjust sigmoid parameters for better distribution
        return 1 / (1 + math.exp(-3 * x))  # Reduced scale for smoother transition

    def sensitivity_analysis(self, financials: Dict[str, Any], variation: float = 0.2) -> Dict[str, float]:
        """Perform sensitivity analysis by varying component weights.
        
        Args:
            financials: Organization's financial data
            variation: Percentage variation to apply to weights (default: 0.2 or 20%)
            
        Returns:
            Dictionary mapping each component to its sensitivity score
        """
        base_score, _ = self.calculate_aem(financials)
        results = {}
        
        # Test each component weight
        for metric in self.base_weights:
            # Create modified calculator with adjusted weight
            modified_weights = self.base_weights.copy()
            modified_weights[metric] *= (1 + variation)
            modified_calc = AEMCalculator()
            modified_calc.base_weights = modified_weights
            
            # Calculate new score
            new_score, _ = modified_calc.calculate_aem(financials)
            results[metric] = abs(new_score - base_score)
        
        return results

    def analyze_components(self, financials: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how each component contributes to the final score.
        
        Args:
            financials: Organization's financial data
            
        Returns:
            Dictionary containing total score, component scores, and contributions
        """
        score, components = self.calculate_aem(financials)
        
        # Calculate contribution of each component
        contributions = {}
        for metric, comp_score in components.items():
            weight = self.base_weights[metric]
            contributions[metric] = weight * comp_score
        
        return {
            'total_score': score,
            'component_scores': components,
            'contributions': contributions
        }

    def analyze_normalization(self, financials: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how normalization affects each metric.
        
        Args:
            financials: Organization's financial data
            
        Returns:
            Dictionary containing raw metrics, normalized metrics, and final score
        """
        # Get raw metrics before normalization
        raw_metrics = {
            'program_expense_ratio': self._calculate_program_expense_ratio(financials),
            'fundraising_efficiency': self._calculate_fundraising_efficiency(financials),
            'revenue_sustainability': self._calculate_revenue_sustainability(financials),
            'net_surplus_margin': self._calculate_net_surplus_margin(financials),
            'executive_pay_reasonableness': self._calculate_executive_pay_reasonableness(financials),
            'transparency': self._fuzzy_policy_evaluation(financials.get('policies', {}))
        }
        
        # Get normalized scores
        score, normalized_metrics = self.calculate_aem(financials)
        
        return {
            'raw_metrics': raw_metrics,
            'normalized_metrics': normalized_metrics,
            'final_score': score
        }

    def cross_validate_schools(self, school1_data: Dict[str, Any], school2_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare AEM scores between two schools.
        
        Args:
            school1_data: First school's financial data
            school2_data: Second school's financial data
            
        Returns:
            Dictionary containing scores and components for both schools
        """
        # Calculate scores for both schools
        school1_score, school1_components = self.calculate_aem(school1_data)
        school2_score, school2_components = self.calculate_aem(school2_data)
        
        return {
            school1_data['organization_name']: {'score': school1_score, 'components': school1_components},
            school2_data['organization_name']: {'score': school2_score, 'components': school2_components}
        } 