import { useEffect } from 'react';

export default function TiktokLogin() {
    const handleLogin = () => {
        const tiktok_client_key = process.env.tiktok_client_key;
        const redirectUri = `${window.location.origin}/callback`;
    
        const tiktokAuthUrl = `https://www.tiktok.com/auth/authorize/?client_key=${tiktok_client_key}&scope=user.info.basic&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}`;
    
        window.location.href = tiktokAuthUrl;
      };
    
      return (
        <div className="flex items-center justify-center h-screen">
          <button
            onClick={handleLogin}
            className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
          >
            Login with TikTok
          </button>
        </div>
      );
}