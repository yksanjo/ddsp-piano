#!/usr/bin/env python3
"""SAP License Optimizer"""

class LicenseOptimizer:
    def analyze(self):
        return {"savings": "$50K/year", "unused": 15}

if __name__ == '__main__':
    opt = LicenseOptimizer()
    print(opt.analyze())

