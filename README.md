# Altruistic Effectiveness Metric (AEM) Calculator

The AEM Calculator is a tool designed to evaluate the effectiveness of nonprofit organizations based on their financial data from Form 990 filings. It provides a quantitative measure of how effectively an organization uses its resources to achieve its mission.

## How the Model Works

The AEM score is calculated using six key components, each weighted according to its importance:

1. **Program Expense Ratio (30%)**
   - Measures what percentage of total expenses goes directly to programs
   - Formula: Total Program Expenses / Total Expenses

2. **Fundraising Efficiency (20%)**
   - Evaluates how effectively fundraising dollars are used
   - Formula: Contributions and Grants / Fundraising Expenses
   - Normalized to a 0-1 scale (capped at 10:1 ratio)

3. **Revenue Sustainability (15%)**
   - Assesses the stability of revenue sources
   - Formula: Program Service Revenue / Total Revenue

4. **Net Surplus Margin (15%)**
   - Indicates financial health and sustainability
   - Formula: (Total Revenue - Total Expenses) / Total Revenue

5. **Executive Pay Reasonableness (10%)**
   - Evaluates the proportion of expenses going to executive compensation
   - Formula: 1 - (Top Salary / Total Expenses)

6. **Transparency (10%)**
   - Measures implementation of key governance policies
   - Formula: Number of Implemented Policies / Total Policies

## How to Use

### Prerequisites
- Python 3.6 or higher
- JSON data file containing organization's financial information

### Installation
1. Clone this repository
2. Ensure you have the required files:
   - `main.py`
   - `aem_calculator.py`

### Running the Calculator

1. Prepare your data file:
   - Create a JSON file with the required financial data
   - See `SSA_fixed.json` for an example of the required format

2. Run the calculator:
   ```bash
   python main.py your_data_file.json
   ```

### Required Data Fields

Your JSON file should include these key fields:
```json
{
    "organization_name": "Organization Name",
    "total_revenue": number,
    "total_expenses": number,
    "contributions_and_grants": number,
    "program_service_revenue": number,
    "fundraising_expenses": number,
    "largest_program_expenses": {
        "program_name": {
            "expenses": number
        }
    },
    "top_individual_salaries": {
        "position": salary
    },
    "policies": {
        "policy_name": boolean
    }
}
```

### Interpreting Results

The AEM score ranges from 0 to 1:
- 0.9-1.0: Excellent effectiveness
- 0.8-0.89: Very good effectiveness
- 0.7-0.79: Good effectiveness
- 0.6-0.69: Average effectiveness
- Below 0.6: Needs improvement

## Example

```bash
python main.py SSA_fixed.json
```

Output:
```
AEM Analysis Results:
Organization: Shady Side Academy
AEM Score: 0.750
```

## Customizing the Model

You can modify the weights in `aem_calculator.py` to emphasize different aspects of organizational effectiveness:

```python
custom_weights = {
    'program_expense_ratio': 0.4,
    'fundraising_efficiency': 0.2,
    'revenue_sustainability': 0.1,
    'net_surplus_margin': 0.1,
    'executive_pay_reasonableness': 0.1,
    'transparency': 0.1
}
calculator = AEMCalculator(weights=custom_weights)
```

## Limitations

1. The model relies on accurate and complete financial data
2. Some components may not be applicable to all organizations
3. The weights are based on general nonprofit best practices and may need adjustment for specific sectors
4. The model doesn't account for qualitative factors like program impact

## Contributing

Feel free to submit issues or pull requests to improve the model or add new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
