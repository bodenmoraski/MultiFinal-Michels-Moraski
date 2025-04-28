from typing import Dict, Any

class AEMCalculator:
    def __init__(self, weights: Dict[str, float] = None):
        """Initialize the AEM calculator with optional custom weights.
        
        Args:
            weights: Dictionary of custom weights for each factor. If None, uses default weights.
        """
        self.weights = weights or {
            'program_expense_ratio': 0.3,
            'fundraising_efficiency': 0.2,
            'revenue_sustainability': 0.15,
            'net_surplus_margin': 0.15,
            'executive_pay_reasonableness': 0.1,
            'transparency': 0.1
        }

    def calculate_aem(self, financials: Dict[str, Any]) -> float:
        """Calculate the Altruistic Effectiveness Metric (AEM) score."""
        # Extract Features
        program_expense_ratio = self._calculate_program_expense_ratio(financials)
        fundraising_efficiency = self._calculate_fundraising_efficiency(financials)
        revenue_sustainability = self._calculate_revenue_sustainability(financials)
        net_surplus_margin = self._calculate_net_surplus_margin(financials)
        executive_pay_reasonableness = self._calculate_executive_pay_reasonableness(financials)
        transparency = self._calculate_transparency(financials)

        # Weighted Sum
        aem_score = (
            self.weights['program_expense_ratio'] * program_expense_ratio +
            self.weights['fundraising_efficiency'] * fundraising_efficiency +
            self.weights['revenue_sustainability'] * revenue_sustainability +
            self.weights['net_surplus_margin'] * net_surplus_margin +
            self.weights['executive_pay_reasonableness'] * executive_pay_reasonableness +
            self.weights['transparency'] * transparency
        )

        return aem_score

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
        return min(efficiency, 10) / 10  # Normalize to 0-1 range

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
        """Calculate the reasonableness of executive pay."""
        if not financials.get('top_individual_salaries') or financials['total_expenses'] == 0:
            return 1.0
        
        top_salary = max(financials['top_individual_salaries'].values())
        return 1 - (top_salary / financials['total_expenses'])

    def _calculate_transparency(self, financials: Dict[str, Any]) -> float:
        """Calculate the transparency score based on policy implementation."""
        if not financials.get('policies'):
            return 0.0
        return sum(1 for p in financials['policies'].values() if p) / len(financials['policies']) 