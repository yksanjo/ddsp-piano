import React, { useState } from 'react';
import { Shuffle, Key, Dice1 } from 'lucide-react';
import { QuantumRandom } from '../utils/quantumSimulator';

const QuantumRandomDemo = () => {
  const [randomBits, setRandomBits] = useState([]);
  const [randomNumber, setRandomNumber] = useState(null);
  const [password, setPassword] = useState('');
  const [diceRolls, setDiceRolls] = useState([]);

  const generateBits = () => {
    const bits = QuantumRandom.generateBits(8);
    setRandomBits(bits);
  };

  const generateNumber = () => {
    const num = QuantumRandom.generateNumber(1, 100);
    setRandomNumber(num);
  };

  const generatePassword = () => {
    const pwd = QuantumRandom.generatePassword(12);
    setPassword(pwd);
  };

  const rollDice = () => {
    const rolls = [];
    for (let i = 0; i < 5; i++) {
      rolls.push(QuantumRandom.generateNumber(1, 6));
    }
    setDiceRolls(rolls);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8">
      <div className="flex items-center gap-3 mb-6">
        <Shuffle className="w-8 h-8 text-quantum-purple" />
        <h2 className="text-2xl font-bold text-gray-800">Quantum Randomness</h2>
      </div>

      <p className="text-gray-600 mb-8 text-lg">
        Classical computers use pseudo-random algorithms (predictable patterns). 
        Quantum computers generate <strong>true randomness</strong> from quantum measurements — 
        used in real security systems!
      </p>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Random Bits */}
        <div className="border-2 border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <Dice1 className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-700">Random Bits</h3>
          </div>
          <div className="flex gap-2 mb-4 min-h-[60px] items-center justify-center">
            {randomBits.length > 0 ? (
              randomBits.map((bit, i) => (
                <div
                  key={i}
                  className={`w-12 h-12 rounded-lg flex items-center justify-center text-xl font-bold transition-all ${
                    bit === 0 ? 'bg-blue-500 text-white' : 'bg-pink-500 text-white'
                  }`}
                >
                  {bit}
                </div>
              ))
            ) : (
              <p className="text-gray-400">Click to generate</p>
            )}
          </div>
          <button
            onClick={generateBits}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Generate 8 Bits
          </button>
        </div>

        {/* Random Number */}
        <div className="border-2 border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <Dice1 className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-700">Random Number (1-100)</h3>
          </div>
          <div className="text-center mb-4 min-h-[60px] flex items-center justify-center">
            {randomNumber !== null ? (
              <p className="text-4xl font-bold text-gray-800">{randomNumber}</p>
            ) : (
              <p className="text-gray-400">Click to generate</p>
            )}
          </div>
          <button
            onClick={generateNumber}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Generate Number
          </button>
        </div>

        {/* Password Generator */}
        <div className="border-2 border-quantum-purple rounded-lg p-6 bg-purple-50">
          <div className="flex items-center gap-2 mb-4">
            <Key className="w-5 h-5 text-quantum-purple" />
            <h3 className="text-lg font-semibold text-quantum-purple">Secure Password</h3>
          </div>
          <div className="mb-4 min-h-[60px] flex items-center justify-center">
            {password ? (
              <p className="text-xl font-mono font-bold text-gray-800 break-all text-center">
                {password}
              </p>
            ) : (
              <p className="text-gray-400">Click to generate</p>
            )}
          </div>
          <button
            onClick={generatePassword}
            className="w-full bg-quantum-purple hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Generate Password
          </button>
        </div>

        {/* Dice Rolls */}
        <div className="border-2 border-gray-200 rounded-lg p-6">
          <div className="flex items-center gap-2 mb-4">
            <Dice1 className="w-5 h-5 text-gray-600" />
            <h3 className="text-lg font-semibold text-gray-700">Dice Rolls</h3>
          </div>
          <div className="flex gap-2 mb-4 min-h-[60px] items-center justify-center">
            {diceRolls.length > 0 ? (
              diceRolls.map((roll, i) => (
                <div
                  key={i}
                  className="w-16 h-16 rounded-lg bg-blue-500 text-white flex items-center justify-center text-2xl font-bold"
                >
                  {roll}
                </div>
              ))
            ) : (
              <p className="text-gray-400">Click to roll</p>
            )}
          </div>
          <button
            onClick={rollDice}
            className="w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
          >
            Roll 5 Dice
          </button>
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
        <p className="text-blue-800 text-sm">
          <strong>💡 Real-World Use:</strong> Quantum randomness is used in cryptography, 
          secure key generation, and lottery systems where true unpredictability is essential!
        </p>
      </div>
    </div>
  );
};

export default QuantumRandomDemo;



