// api.js – front‑end helper to call the serverless AI endpoint
// ---------------------------------------------------------------
// The endpoint URL must be set as an environment variable in the static site
// or hard‑coded here for the prototype. Replace YOUR_ENDPOINT_URL with the
// actual URL of the deployed serverless function (e.g. Vercel or Netlify).

export async function callAI(prompt) {
  const endpoint = "https://copiloto-vendas-omega.vercel.app/api/generate"; // updated after Vercel deployment
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    });
    if (!response.ok) {
      const err = await response.text();
      throw new Error('API error: ' + err);
    }
    const data = await response.json();
    return data.result; // expected shape { result: "..." }
  } catch (e) {
    console.error("callAI error:", e);
    throw e;
  }
}
