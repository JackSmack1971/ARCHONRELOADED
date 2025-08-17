'use client';

import { useEffect, useState } from 'react';
import Header from '../components/Header';
import { apiGet, ApiError } from '../services/apiClient';

export default function Page() {
  const [data, setData] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const load = async () => {
      try {
        const res = await apiGet('/status');
        setData(JSON.stringify(res));
      } catch (err) {
        setError((err as ApiError).message);
      }
    };
    void load();
  }, []);

  return (
    <main>
      <Header />
      {error && <p role='alert'>{error}</p>}
      {data && <pre>{data}</pre>}
    </main>
  );
}
