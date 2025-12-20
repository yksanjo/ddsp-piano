#!/usr/bin/env python3
"""
SAP Transaction Code Finder - Web Interface
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from finder import TransactionFinder

app = Flask(__name__)
CORS(app)
finder = TransactionFinder()


@app.route('/')
def index():
    """Main search interface"""
    return render_template('index.html')


@app.route('/api/search', methods=['GET'])
def search():
    """Search API"""
    query = request.args.get('q', '')
    module = request.args.get('module')
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    results = finder.search(query, module=module, limit=limit)
    
    return jsonify({
        'results': [
            {
                'code': tx.code,
                'description': tx.description,
                'module': tx.module,
                'type': tx.transaction_type,
                'category': tx.category,
                'usage': tx.usage_frequency
            }
            for tx in results
        ],
        'count': len(results)
    })


@app.route('/api/transaction/<code>', methods=['GET'])
def get_transaction(code):
    """Get transaction details"""
    tx = finder.get_transaction(code)
    if not tx:
        return jsonify({'error': 'Transaction not found'}), 404
    
    return jsonify({
        'code': tx.code,
        'description': tx.description,
        'module': tx.module,
        'type': tx.transaction_type,
        'category': tx.category,
        'usage': tx.usage_frequency,
        'related': tx.related_codes
    })


@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Get all modules"""
    modules = set(tx.module for tx in finder.transactions)
    return jsonify({'modules': sorted(modules)})


@app.route('/api/popular', methods=['GET'])
def get_popular():
    """Get popular transactions"""
    limit = int(request.args.get('limit', 10))
    transactions = finder.get_popular(limit)
    
    return jsonify({
        'transactions': [
            {
                'code': tx.code,
                'description': tx.description,
                'module': tx.module,
                'usage': tx.usage_frequency
            }
            for tx in transactions
        ]
    })


if __name__ == '__main__':
    print("🚀 Starting SAP Transaction Code Finder")
    print("📱 Open http://localhost:5000")
    app.run(debug=True, port=5000)

