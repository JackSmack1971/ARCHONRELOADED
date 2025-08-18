import React from 'react';
import { Button } from '../components/atoms/Button';

export const Home: React.FC = () => {
  const handleClick = () => {
    console.log('Button clicked');
  };

  return (
    <div>
      <h1>Archon UI</h1>
      <Button variant="primary" onClick={handleClick}>
        Click me
      </Button>
    </div>
  );
};
