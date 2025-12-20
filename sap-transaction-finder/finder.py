#!/usr/bin/env python3
"""
SAP Transaction Code Finder
Search and find SAP transaction codes by description or keywords
"""

import json
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Transaction:
    """SAP Transaction model"""
    code: str
    description: str
    module: str
    transaction_type: str  # display, create, change, etc.
    category: Optional[str] = None
    usage_frequency: int = 0
    related_codes: List[str] = None
    
    def __post_init__(self):
        if self.related_codes is None:
            self.related_codes = []


class TransactionFinder:
    """Find SAP transaction codes"""
    
    def __init__(self):
        self.transactions = []
        self._load_transactions()
    
    def _load_transactions(self):
        """Load transaction database"""
        # Sample transaction database
        sample_transactions = [
            # Financial Accounting (FI)
            Transaction("FBL1N", "Display Vendor Line Items", "FI", "display", "Accounts Payable", 1000),
            Transaction("FBL3N", "Display G/L Account Line Items", "FI", "display", "General Ledger", 950),
            Transaction("FB03", "Display Document", "FI", "display", "Document", 1200),
            Transaction("FB01", "Enter Document", "FI", "create", "Document", 800),
            Transaction("FB02", "Change Document", "FI", "change", "Document", 200),
            Transaction("F-02", "Enter G/L Account Posting", "FI", "create", "General Ledger", 600),
            Transaction("F-43", "Enter Vendor Invoice", "FI", "create", "Accounts Payable", 700),
            Transaction("F-22", "Enter Customer Invoice", "FI", "create", "Accounts Receivable", 650),
            
            # Sales & Distribution (SD)
            Transaction("VA01", "Create Sales Order", "SD", "create", "Sales Order", 900),
            Transaction("VA02", "Change Sales Order", "SD", "change", "Sales Order", 500),
            Transaction("VA03", "Display Sales Order", "SD", "display", "Sales Order", 1100),
            Transaction("VA05", "List of Sales Orders", "SD", "display", "Sales Order", 850),
            Transaction("VL01N", "Create Outbound Delivery", "SD", "create", "Delivery", 750),
            Transaction("VF01", "Create Billing Document", "SD", "create", "Billing", 800),
            Transaction("VD01", "Create Customer", "SD", "create", "Master Data", 400),
            Transaction("VD03", "Display Customer", "SD", "display", "Master Data", 600),
            
            # Materials Management (MM)
            Transaction("ME21N", "Create Purchase Order", "MM", "create", "Purchase Order", 850),
            Transaction("ME22N", "Change Purchase Order", "MM", "change", "Purchase Order", 400),
            Transaction("ME23N", "Display Purchase Order", "MM", "display", "Purchase Order", 1000),
            Transaction("ME51N", "Create Purchase Requisition", "MM", "create", "Requisition", 600),
            Transaction("MM01", "Create Material", "MM", "create", "Master Data", 500),
            Transaction("MM03", "Display Material", "MM", "display", "Master Data", 900),
            Transaction("MMBE", "Stock Overview", "MM", "display", "Inventory", 1100),
            Transaction("MB52", "List of Material Stocks", "MM", "display", "Inventory", 800),
            
            # Controlling (CO)
            Transaction("KS01", "Create Cost Center", "CO", "create", "Cost Center", 300),
            Transaction("KS03", "Display Cost Center", "CO", "display", "Cost Center", 500),
            Transaction("KB11N", "Enter Cost Center Activity", "CO", "create", "Activity", 200),
            Transaction("S_ALR_87013611", "Cost Center Reports", "CO", "display", "Reports", 400),
            
            # Human Resources (HR)
            Transaction("PA30", "Maintain HR Master Data", "HR", "change", "Master Data", 400),
            Transaction("PA20", "Display HR Master Data", "HR", "display", "Master Data", 600),
            Transaction("PA40", "Personnel Actions", "HR", "create", "Actions", 300),
            
            # Production Planning (PP)
            Transaction("CO01", "Create Production Order", "PP", "create", "Production", 500),
            Transaction("CO03", "Display Production Order", "PP", "display", "Production", 700),
            Transaction("MD04", "Stock/Requirements List", "PP", "display", "Planning", 800),
            
            # Plant Maintenance (PM)
            Transaction("IW31", "Create Maintenance Order", "PM", "create", "Maintenance", 300),
            Transaction("IW33", "Display Maintenance Order", "PM", "display", "Maintenance", 400),
        ]
        
        self.transactions = sample_transactions
    
    def search(self, query: str, module: Optional[str] = None, limit: int = 20) -> List[Transaction]:
        """Search transactions"""
        query_lower = query.lower()
        results = []
        
        for tx in self.transactions:
            # Filter by module
            if module and tx.module != module:
                continue
            
            # Score based on matches
            score = 0
            
            # Exact code match
            if query_lower == tx.code.lower():
                score += 1000
            
            # Code contains query
            if query_lower in tx.code.lower():
                score += 500
            
            # Description contains query
            if query_lower in tx.description.lower():
                score += 100
            
            # Keywords match
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in tx.description.lower():
                    score += 50
                if keyword in tx.category.lower() if tx.category else False:
                    score += 30
            
            if score > 0:
                results.append((score, tx))
        
        # Sort by score
        results.sort(key=lambda x: x[0], reverse=True)
        return [tx for _, tx in results[:limit]]
    
    def get_transaction(self, code: str) -> Optional[Transaction]:
        """Get transaction by code"""
        code_upper = code.upper()
        for tx in self.transactions:
            if tx.code.upper() == code_upper:
                return tx
        return None
    
    def get_by_module(self, module: str) -> List[Transaction]:
        """Get all transactions for a module"""
        return [tx for tx in self.transactions if tx.module == module]
    
    def get_popular(self, limit: int = 10) -> List[Transaction]:
        """Get most popular transactions"""
        sorted_tx = sorted(self.transactions, key=lambda x: x.usage_frequency, reverse=True)
        return sorted_tx[:limit]


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='SAP Transaction Code Finder')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--code', '-c', help='Get transaction by code')
    parser.add_argument('--module', '-m', help='Filter by module (FI, CO, SD, MM, etc.)')
    parser.add_argument('--module-list', action='store_true', help='List all transactions for a module')
    parser.add_argument('--popular', action='store_true', help='Show popular transactions')
    
    args = parser.parse_args()
    
    finder = TransactionFinder()
    
    if args.code:
        tx = finder.get_transaction(args.code)
        if tx:
            print(f"\n📋 {tx.code} - {tx.description}")
            print(f"   Module: {tx.module}")
            print(f"   Type: {tx.transaction_type}")
            print(f"   Category: {tx.category}")
            print(f"   Usage: {tx.usage_frequency}")
        else:
            print(f"❌ Transaction {args.code} not found")
    
    elif args.module_list and args.module:
        transactions = finder.get_by_module(args.module)
        print(f"\n📚 Transactions for module {args.module}:")
        for tx in transactions:
            print(f"  {tx.code:8} - {tx.description}")
    
    elif args.popular:
        transactions = finder.get_popular()
        print("\n🔥 Most Popular SAP Transactions:")
        for tx in transactions:
            print(f"  {tx.code:8} - {tx.description} ({tx.module})")
    
    elif args.query:
        results = finder.search(args.query, module=args.module)
        if results:
            print(f"\n🔍 Found {len(results)} transaction(s) for '{args.query}':\n")
            for tx in results:
                print(f"  {tx.code:8} - {tx.description}")
                print(f"            Module: {tx.module} | Type: {tx.transaction_type}")
                if tx.category:
                    print(f"            Category: {tx.category}")
                print()
        else:
            print(f"❌ No transactions found for '{args.query}'")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

