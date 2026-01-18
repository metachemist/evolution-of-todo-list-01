"use client";

import { useState, useEffect } from "react";

interface Petal {
  id: number;
  left: number;
  delay: number;
  duration: number;
  size: number;
}

export function CherryBlossom() {
  const [petals, setPetals] = useState<Petal[]>([]);

  useEffect(() => {
    // Generate random petals
    const generatedPetals: Petal[] = Array.from({ length: 15 }, (_, i) => ({
      id: i,
      left: Math.random() * 100,
      delay: Math.random() * 5,
      duration: 3 + Math.random() * 7,
      size: 10 + Math.random() * 20,
    }));
    
    setPetals(generatedPetals);
  }, []);

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
      {petals.map((petal) => (
        <div
          key={petal.id}
          className="absolute rounded-full bg-accent opacity-70 dark:opacity-40"
          style={{
            top: "-50px",
            left: `${petal.left}%`,
            width: `${petal.size}px`,
            height: `${petal.size}px`,
            animation: `float ${petal.duration}s linear ${petal.delay}s infinite, sway 3s ease-in-out ${petal.delay}s infinite alternate`,
          }}
        />
      ))}
    </div>
  );
}