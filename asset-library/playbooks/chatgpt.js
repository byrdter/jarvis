// Playbook: ChatGPT (OpenAI product surface)
//
// Run: node capture-runner.js chatgpt
//
// Notes:
//   - chatgpt.com redirects unauthenticated users to a marketing/landing view.
//   - Authenticated app captures are manual (Cmd+Shift+4 into surfaces/web/).

export default {
  product: 'chatgpt',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://chatgpt.com/',
          wait: 2500,
        },
        {
          type: 'screenshot',
          name: 'hero-full',
          url: 'https://chatgpt.com/',
          fullPage: true,
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'scroll-homepage',
          url: 'https://chatgpt.com/',
          duration: 7,
        },
        {
          type: 'screenshot',
          name: 'login-landing',
          url: 'https://chatgpt.com/auth/login',
          wait: 2500,
        },
      ],
    },
  ],
};
