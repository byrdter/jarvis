// Playbook: Gemini (Google)
//
// Run:  node capture-runner.js gemini
//
// Notes:
//   - gemini.google.com/app typically redirects unauthenticated visitors
//     to the marketing landing. We capture the public landing + features pages.
//   - For an authenticated app screenshot, capture manually with Cmd+Shift+4
//     into products/gemini/surfaces/web/app-authenticated.png.

export default {
  product: 'gemini',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://gemini.google.com/',
          wait: 2500,
        },
        {
          type: 'screenshot',
          name: 'hero-full',
          url: 'https://gemini.google.com/',
          fullPage: true,
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'scroll-homepage',
          url: 'https://gemini.google.com/',
          duration: 8,
        },
        {
          type: 'screenshot',
          name: 'app-landing',
          url: 'https://gemini.google.com/app',
          wait: 3000,
        },
      ],
    },
  ],
};
