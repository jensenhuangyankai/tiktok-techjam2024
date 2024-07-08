import { NextResponse } from 'next/server';

export async function POST(req) {
  const { code } = await req.json();

  const response = await fetch('https://open-api.tiktok.com/oauth/access_token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      client_key: process.env.tiktok_client_key,
      client_secret: process.env.tiktok_client_secret,
      code,
      grant_type: 'authorization_code',
      redirect_uri: `${req.headers.origin}/callback`,
    }),
  });

  const data = await response.json();
  return NextResponse.json(data);
}