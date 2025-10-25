// src/components/ParticlesBg.jsx
import React from 'react';
import { loadFull } from 'tsparticles';
import { useCallback } from 'react';
import Particles from 'react-tsparticles';

const ParticlesBg = () => {
  const particlesInit = useCallback(async engine => {
    await loadFull(engine);
  }, []);

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      options={{
        fullScreen: { enable: false },
        background: { color: 'transparent' },
        particles: {
          number: { value: 80 },
          color: { value: '#00ffc3' },
          shape: { type: 'circle' },
          opacity: { value: 0.4 },
          size: { value: 3 },
          move: { enable: true, speed: 1 },
        },
        interactivity: {
          events: { onHover: { enable: true, mode: 'repulse' } },
          modes: { repulse: { distance: 100 } },
        },
      }}
    />
  );
};

export default ParticlesBg;
