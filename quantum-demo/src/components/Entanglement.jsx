import React, { useState } from 'react';
import { Link, Zap, Eye } from 'lucide-react';
import { EntangledPair } from '../utils/quantumSimulator';

const Entanglement = () => {
  const [pair] = useState(() => new EntangledPair());
  const [qubitA, setQubitA] = useState(null);
  const [qubitB, setQubitB] = useState(null);
  const [distance, setDistance] = useState(50);
  const [isMeasured, setIsMeasured] = useState(false);

  const createEntanglement = () => {
    pair.reset();
    setQubitA(null);
    setQubitB(null);
    setIsMeasured(false);
  };

  const measureA = () => {
    const result = pair.measureA();
    setQubitA(result);
    setQubitB(pair.measurementB);
    setIsMeasured(true);
  };

  const measureB = () => {
    const result = pair.measureB();
    setQubitB(result);
    setQubitA(pair.measurementA);
    setIsMeasured(true);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex items-center gap-3 mb-6">
        <Link className="w-8 h-8 text-quantum-purple" />
        <h2 className="text-2xl font-bold text-gray-800">Quantum Entanglement: "Quantum Twins"</h2>
      </div>

      <p className="text-gray-600 mb-8 text-lg">
        Two qubits become "entangled" — they act like one system, even when far apart. 
        Measure one, and the other instantly knows!
      </p>

      {/* Distance Slider */}
      <div className="mb-8">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Distance Between Qubits: {distance} km
        </label>
        <input
          type="range"
          min="1"
          max="100"
          value={distance}
          onChange={(e) => setDistance(Number(e.target.value))}
          className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
        />
        <p className="text-xs text-gray-500 mt-1">
          Distance doesn't matter — correlation is instant!
        </p>
      </div>

      {/* Visual Representation */}
      <div className="relative mb-8" style={{ height: '200px' }}>
        {/* Connection Line */}
        <svg className="absolute inset-0 w-full h-full" style={{ zIndex: 1 }}>
          <line
            x1="10%"
            y1="50%"
            x2="90%"
            y2="50%"
            stroke={isMeasured && qubitA === qubitB ? '#8b5cf6' : '#e5e7eb'}
            strokeWidth="3"
            strokeDasharray={isMeasured ? "0" : "5,5"}
            className="transition-all duration-500"
          />
          {isMeasured && qubitA === qubitB && (
            <animate attributeName="stroke" values="#e5e7eb;#8b5cf6" dur="0.5s" />
          )}
        </svg>

        {/* Qubit A */}
        <div className="absolute left-0 top-1/2 transform -translate-y-1/2">
          <div className={`w-20 h-20 rounded-full flex items-center justify-center text-2xl font-bold transition-all duration-500 ${
            qubitA === null 
              ? 'bg-gray-200 text-gray-400' 
              : qubitA === 0 
                ? 'bg-blue-500 text-white' 
                : 'bg-pink-500 text-white'
          }`}>
            {qubitA === null ? '?' : qubitA}
          </div>
          <p className="text-xs text-center mt-2 text-gray-600">Qubit A</p>
          {!isMeasured && (
            <button
              onClick={measureA}
              className="mt-2 bg-quantum-blue hover:bg-blue-600 text-white text-xs font-semibold py-1 px-3 rounded transition-colors flex items-center gap-1"
            >
              <Eye className="w-3 h-3" />
              Measure
            </button>
          )}
        </div>

        {/* Qubit B */}
        <div className="absolute right-0 top-1/2 transform -translate-y-1/2">
          <div className={`w-20 h-20 rounded-full flex items-center justify-center text-2xl font-bold transition-all duration-500 ${
            qubitB === null 
              ? 'bg-gray-200 text-gray-400' 
              : qubitB === 0 
                ? 'bg-blue-500 text-white' 
                : 'bg-pink-500 text-white'
          }`}>
            {qubitB === null ? '?' : qubitB}
          </div>
          <p className="text-xs text-center mt-2 text-gray-600">Qubit B</p>
          {!isMeasured && (
            <button
              onClick={measureB}
              className="mt-2 bg-quantum-blue hover:bg-blue-600 text-white text-xs font-semibold py-1 px-3 rounded transition-colors flex items-center gap-1"
            >
              <Eye className="w-3 h-3" />
              Measure
            </button>
          )}
        </div>
      </div>

      {/* Controls */}
      <div className="flex justify-center gap-4">
        <button
          onClick={createEntanglement}
          className="bg-quantum-purple hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors flex items-center gap-2"
        >
          <Zap className="w-4 h-4" />
          Create Entangled Pair
        </button>
      </div>

      {/* Results */}
      {isMeasured && (
        <div className="mt-6 p-4 bg-green-50 border-l-4 border-green-500 rounded">
          <p className="text-green-800 text-sm">
            <strong>✨ Correlation Detected!</strong> Both qubits measured the same value ({qubitA}) 
            instantly, even though they're {distance} km apart. They act like one system!
          </p>
        </div>
      )}

      <div className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
        <p className="text-blue-800 text-sm">
          <strong>💡 Wow Moment:</strong> The information appears at qubit B without traveling through space. 
          This is called "quantum non-locality" and it's real!
        </p>
      </div>
    </div>
  );
};

export default Entanglement;



