import argparse
import json
from aem_calculator import AEMCalculator

def load_financial_data(file_path: str) -> dict:
    """Load financial data from a JSON file.
    
    Args:
        file_path: Path to the JSON file containing financial data
        
    Returns:
        dict: Financial data dictionary
    """
    with open(file_path, 'r') as file:
        return json.load(file)

def main(input_file: str):
    # Load financial data
    financials = load_financial_data(input_file)
    
    # Calculate AEM score
    calculator = AEMCalculator()
    aem_score = calculator.calculate_aem(financials)
    
    print(f"AEM Score: {aem_score:.3f}")
    print(f"Organization: {financials.get('organization_name', 'Unknown')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate AEM score for a given financial data file.')
    parser.add_argument('input_file', type=str, help='Path to the financial data file (JSON format)')
    args = parser.parse_args()
    main(args.input_file)



    


        
        