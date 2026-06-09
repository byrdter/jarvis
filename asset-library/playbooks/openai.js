// Playbook: OpenAI (corporate / platform surfaces)
//
// Run: node capture-runner.js openai
//
// Use these for "OpenAI as a company" b-roll, distinct from chatgpt product UI.

export default {
  product: 'openai',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://openai.com/',
          wait: 2500,
        },
        {
          type: 'screenshot',
          name: 'hero-full',
          url: 'https://openai.com/',
          fullPage: true,
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'scroll-homepage',
          url: 'https://openai.com/',
          duration: 7,
        },
        {
          type: 'screenshot',
          name: 'platform',
          url: 'https://platform.openai.com/',
          wait: 2500,
        },
        {
          type: 'screenshot',
          name: 'pricing',
          url: 'https://openai.com/pricing/',
          wait: 2500,
        },
      ],
    },
  ],
};
