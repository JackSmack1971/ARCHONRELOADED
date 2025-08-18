import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { Button } from '../src/components/atoms/Button';

describe('Button', () => {
  it('calls onClick when clicked', () => {
    const onClick = vi.fn();
    render(<Button variant="primary" onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText(/click/i));
    expect(onClick).toHaveBeenCalled();
  });
});
