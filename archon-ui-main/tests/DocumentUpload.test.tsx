import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { DocumentUpload } from '../src/features/documents/DocumentUpload';
import * as hook from '../src/hooks/useUploadDocument';
import { describe, it, expect, vi } from 'vitest';

describe('DocumentUpload', () => {
  it('uploads file', async () => {
    const mutateAsync = vi.fn().mockResolvedValue({ id: 'd1', name: 't.txt' });
    vi.spyOn(hook, 'useUploadDocument').mockReturnValue({
      mutateAsync,
      isPending: false,
      error: null,
    } as ReturnType<typeof hook.useUploadDocument>);
    const client = new QueryClient();
    render(
      <QueryClientProvider client={client}>
        <DocumentUpload projectId="p1" />
      </QueryClientProvider>,
    );
    const file = new File(['data'], 't.txt', { type: 'text/plain' });
    fireEvent.change(screen.getByLabelText('file'), { target: { files: [file] } });
    fireEvent.click(screen.getByRole('button', { name: /upload/i }));
    await waitFor(() => expect(mutateAsync).toHaveBeenCalled());
  });
});
