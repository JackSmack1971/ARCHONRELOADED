import React, { useState } from 'react';
import { useSearch } from '../../hooks/useSearch';

export const SearchResults: React.FC = () => {
  const [query, setQuery] = useState('');
  const { data, error } = useSearch(query);

  return (
    <div>
      <input aria-label="search" value={query} onChange={(e) => setQuery(e.target.value)} />
      {error && <div role="alert">{error.message}</div>}
      <ul>
        {data?.map((r) => (
          <li key={r.id}>
            <strong>{r.title}</strong>
            <p>{r.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};
