import React, { useState } from 'react';
import { ProjectForm } from '../features/projects/ProjectForm';
import { DocumentUpload } from '../features/documents/DocumentUpload';
import { SearchResults } from '../features/search/SearchResults';

export const Home: React.FC = () => {
  const [projectId, setProjectId] = useState('');

  return (
    <div>
      <h1>Archon UI</h1>
      <ProjectForm onCreated={setProjectId} />
      <DocumentUpload projectId={projectId} />
      <SearchResults />
    </div>
  );
};
