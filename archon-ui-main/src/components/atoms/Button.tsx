import React from 'react';

interface ButtonProps {
  variant: 'primary' | 'secondary';
  children: React.ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({ variant, children, onClick, disabled = false }) => (
  <button className={`btn btn--${variant}`} onClick={onClick} disabled={disabled}>
    {children}
  </button>
);
