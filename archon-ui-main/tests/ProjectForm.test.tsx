import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ProjectForm } from '../src/features/projects/ProjectForm';
import * as hook from '../src/hooks/useCreateProject';
import { describe, it, expect, vi } from 'vitest';

describe('ProjectForm', () => {
  it('submits project data', async () => {
    const mutateAsync = vi.fn().mockResolvedValue({ id: '1', name: 'a', description: 'b' });
    vi.spyOn(hook, 'useCreateProject').mockReturnValue({
      mutateAsync,
      isPending: false,
      error: null,
    } as ReturnType<typeof hook.useCreateProject>);
    const onCreated = vi.fn();
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <ProjectForm onCreated={onCreated} />
      </QueryClientProvider>,
    );
    fireEvent.change(screen.getByLabelText('name'), { target: { value: 'a' } });
    fireEvent.change(screen.getByLabelText('description'), { target: { value: 'b' } });
    fireEvent.click(screen.getByRole('button', { name: /create/i }));
    await waitFor(() => expect(mutateAsync).toHaveBeenCalled());
  });
});
