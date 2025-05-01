import json
from aem_calculator import AEMCalculator

def run_validation():
    # Load the financial data
    with open('data/Episcopal.json', 'r') as f:
        episcopal_data = json.load(f)
    with open('data/Haverford.json', 'r') as f:
        haverford_data = json.load(f)
    
    calculator = AEMCalculator()
    
    # 1. Sensitivity Analysis
    print("\nSensitivity Analysis for Episcopal Academy:")
    sensitivity_results = calculator.sensitivity_analysis(episcopal_data)
    for metric, sensitivity in sensitivity_results.items():
        print(f"{metric}: {sensitivity:.4f}")
    
    # 2. Component Analysis
    print("\nComponent Analysis for Episcopal Academy:")
    component_results = calculator.analyze_components(episcopal_data)
    print(f"Total Score: {component_results['total_score']:.4f}")
    print("\nComponent Scores:")
    for metric, score in component_results['component_scores'].items():
        print(f"{metric}: {score:.4f}")
    print("\nContributions:")
    for metric, contribution in component_results['contributions'].items():
        print(f"{metric}: {contribution:.4f}")
    
    # 3. Normalization Analysis
    print("\nNormalization Analysis for Episcopal Academy:")
    norm_results = calculator.analyze_normalization(episcopal_data)
    print("\nRaw Metrics:")
    for metric, value in norm_results['raw_metrics'].items():
        print(f"{metric}: {value:.4f}")
    print("\nNormalized Metrics:")
    for metric, value in norm_results['normalized_metrics'].items():
        print(f"{metric}: {value:.4f}")
    
    # 4. Cross-validation between schools
    print("\nCross-validation between Philadelphia schools:")
    cross_val_results = calculator.cross_validate_schools(episcopal_data, haverford_data)
    
    # Get the organization names from the data
    episcopal_name = episcopal_data['organization_name']
    haverford_name = haverford_data['organization_name']
    
    print(f"\n{episcopal_name} Results:")
    print(f"Total Score: {cross_val_results[episcopal_name]['score']:.4f}")
    print("Component Scores:")
    for metric, score in cross_val_results[episcopal_name]['components'].items():
        print(f"{metric}: {score:.4f}")
    
    print(f"\n{haverford_name} Results:")
    print(f"Total Score: {cross_val_results[haverford_name]['score']:.4f}")
    print("Component Scores:")
    for metric, score in cross_val_results[haverford_name]['components'].items():
        print(f"{metric}: {score:.4f}")

if __name__ == "__main__":
    run_validation()
