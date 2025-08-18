import React, { useState } from 'react';
import { useUploadDocument } from '../../hooks/useUploadDocument';
import { Button } from '../../components/atoms/Button';

interface Props {
  projectId: string;
}

export const DocumentUpload: React.FC<Props> = ({ projectId }) => {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useUploadDocument();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file || !projectId) return;
    try {
      await mutation.mutateAsync({ projectId, file });
      setFile(null);
    } catch {
      // error handled by mutation
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input aria-label="project-id" value={projectId} readOnly />
      <input
        aria-label="file"
        type="file"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />
      <Button variant="secondary" disabled={mutation.isPending || !projectId}>
        Upload
      </Button>
      {mutation.error && <div role="alert">{mutation.error.message}</div>}
    </form>
  );
};
