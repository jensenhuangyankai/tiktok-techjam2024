'use client';

import { useRouter, useSearchParams } from 'next/navigation';
import { useEffect, Suspense} from 'react';

const CallbackComponent = () => {
    const router = useRouter();
    const searchParams = useSearchParams();
  
    useEffect(() => {
      const fetchAccessToken = async (code) => {
        const response = await fetch('/api/get-access-token', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ code }),
        });
  
        const data = await response.json();
        console.log('Access Token:', data.access_token);
      };
  
      const code = searchParams.get('code');
      if (code) {
        fetchAccessToken(code);
      }
    }, [searchParams]);
  
    return <div>Loading...</div>;
  };
  
  const Callback = () => {
    return (
      <Suspense fallback={<div>Loading...</div>}>
        <CallbackComponent />
      </Suspense>
    );
  };
  
  export default Callback;