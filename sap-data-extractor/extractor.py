#!/usr/bin/env python3
"""SAP Data Extractor"""

class DataExtractor:
    def extract(self, query):
        return {"rows": 1000, "format": "CSV"}

if __name__ == '__main__':
    ext = DataExtractor()
    print(ext.extract("SELECT * FROM KNA1"))

