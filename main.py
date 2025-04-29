import argparse
import json
import os
from aem_calculator import AEMCalculator

def main(input_file: str):
    try:
        # First check if file exists
        if not os.path.exists(input_file):
            print(f"Error: File '{input_file}' not found")
            return
            
        # Try to read the file with explicit encoding
        with open(input_file, 'r', encoding='utf-8') as file:
            financials = json.load(file)
            
            # Calculate AEM score
            calculator = AEMCalculator()
            aem_score, component_scores = calculator.calculate_aem(financials)
            
            print(f"\nAEM Analysis Results:")
            print(f"Organization: {financials.get('organization_name', 'Unknown')}")
            print(f"AEM Score: {aem_score:.3f}")
            print("\nComponent Scores:")
            for metric, score in component_scores.items():
                print(f"{metric.replace('_', ' ').title()}: {score:.3f}")
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {str(e)}")
        print("This might be due to:")
        print("1. The file is not valid JSON")
        print("2. The file might be empty")
        print("3. There might be encoding issues")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Calculate AEM score for a given financial data file.')
    parser.add_argument('input_file', type=str, help='Path to the financial data file (JSON format)')
    args = parser.parse_args()
    main(args.input_file)



    


        
        