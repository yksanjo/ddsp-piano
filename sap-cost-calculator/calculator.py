#!/usr/bin/env python3
"""SAP Cost Calculator"""

class CostCalculator:
    def calculate_tco(self):
        return {"total": "$2M/year", "hidden": "$500K"}

if __name__ == '__main__':
    calc = CostCalculator()
    print(calc.calculate_tco())

