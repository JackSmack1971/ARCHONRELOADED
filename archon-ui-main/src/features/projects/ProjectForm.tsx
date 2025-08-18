import React, { useState } from 'react';
import { useCreateProject } from '../../hooks/useCreateProject';
import { Button } from '../../components/atoms/Button';

interface Props {
  onCreated: (id: string) => void;
}

export const ProjectForm: React.FC<Props> = ({ onCreated }) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const mutation = useCreateProject();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !description.trim()) return;
    try {
      const project = await mutation.mutateAsync({ name, description });
      onCreated(project.id);
      setName('');
      setDescription('');
    } catch {
      // error handled by mutation
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input aria-label="name" value={name} onChange={(e) => setName(e.target.value)} />
      <input
        aria-label="description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <Button variant="primary" disabled={mutation.isPending}>
        Create
      </Button>
      {mutation.error && <div role="alert">{mutation.error.message}</div>}
    </form>
  );
};
