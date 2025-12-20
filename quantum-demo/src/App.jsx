import React, { useState } from 'react';
import { Coins, Link, Search, Shuffle, Menu, X } from 'lucide-react';
import QuantumCoin from './components/QuantumCoin';
import Entanglement from './components/Entanglement';
import GroverSearch from './components/GroverSearch';
import QuantumRandomDemo from './components/QuantumRandom';

const demos = [
  {
    id: 'coin',
    name: 'Quantum Coin',
    icon: Coins,
    component: QuantumCoin,
    description: 'Superposition demo - heads AND tails',
    order: 1
  },
  {
    id: 'entanglement',
    name: 'Quantum Twins',
    icon: Link,
    component: Entanglement,
    description: 'Entanglement - instant correlation',
    order: 2
  },
  {
    id: 'grover',
    name: 'Grover Search',
    icon: Search,
    component: GroverSearch,
    description: 'Faster than classical search',
    order: 3
  },
  {
    id: 'random',
    name: 'Quantum Randomness',
    icon: Shuffle,
    component: QuantumRandomDemo,
    description: 'True randomness generation',
    order: 4
  }
];

function App() {
  const [activeDemo, setActiveDemo] = useState('coin');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const ActiveComponent = demos.find(d => d.id === activeDemo)?.component || QuantumCoin;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <span className="text-white text-xl font-bold">⚛️</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Quantum Computing Demos</h1>
                <p className="text-sm text-gray-600">Interactive learning for non-experts</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="md:hidden p-2 rounded-lg hover:bg-gray-100"
            >
              {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <aside className={`${
            sidebarOpen ? 'block' : 'hidden'
          } md:block w-full md:w-64 flex-shrink-0`}>
            <div className="bg-white rounded-xl shadow-lg p-4 sticky top-8">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Demos</h2>
              <nav className="space-y-2">
                {demos.sort((a, b) => a.order - b.order).map((demo) => {
                  const Icon = demo.icon;
                  const isActive = activeDemo === demo.id;
                  return (
                    <button
                      key={demo.id}
                      onClick={() => {
                        setActiveDemo(demo.id);
                        setSidebarOpen(false);
                      }}
                      className={`w-full flex items-center gap-3 p-3 rounded-lg transition-colors text-left ${
                        isActive
                          ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                          : 'hover:bg-gray-100 text-gray-700'
                      }`}
                    >
                      <Icon className="w-5 h-5 flex-shrink-0" />
                      <div className="flex-1 min-w-0">
                        <div className="font-semibold">{demo.name}</div>
                        <div className={`text-xs ${isActive ? 'text-purple-100' : 'text-gray-500'}`}>
                          {demo.description}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </nav>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Quick Tips</h3>
                <ul className="text-xs text-gray-600 space-y-1">
                  <li>• Each demo runs in 30-60 seconds</li>
                  <li>• Compare quantum vs classical</li>
                  <li>• Look for the "wow" moments!</li>
                </ul>
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 min-w-0">
            <ActiveComponent />
          </main>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Built for educational purposes • Demonstrates quantum computing concepts for non-experts
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;



