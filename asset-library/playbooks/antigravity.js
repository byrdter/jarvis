// Playbook: Antigravity (Google's agentic dev environment)
//
// Run: node capture-runner.js antigravity
//
// Notes:
//   - Antigravity is part of Google Labs; URL may redirect or require auth.
//   - Falls back to labs.google homepage if antigravity.google.com isn't public.

export default {
  product: 'antigravity',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://antigravity.google.com/',
          wait: 3000,
        },
        {
          type: 'screenshot',
          name: 'hero-full',
          url: 'https://antigravity.google.com/',
          fullPage: true,
          wait: 3000,
        },
        {
          type: 'scroll-video',
          name: 'scroll-homepage',
          url: 'https://antigravity.google.com/',
          duration: 7,
        },
        {
          type: 'screenshot',
          name: 'labs-fallback',
          url: 'https://labs.google/',
          wait: 2500,
        },
      ],
    },
  ],
};
