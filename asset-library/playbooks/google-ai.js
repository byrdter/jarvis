// Playbook: Google AI
//
// Run: node capture-runner.js google-ai
//
// Public Gemini, Google AI, AI Studio, and developer documentation surfaces.

export default {
  product: 'google-ai',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://ai.google/',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'homepage-scroll',
          url: 'https://ai.google/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'gemini-docs-scroll',
          url: 'https://ai.google.dev/gemini-api/docs',
          duration: 10,
        },
        {
          type: 'screenshot',
          name: 'ai-studio',
          url: 'https://aistudio.google.com/',
          wait: 3500,
        },
        {
          type: 'scroll-video',
          name: 'blog-scroll',
          url: 'https://blog.google/technology/ai/',
          duration: 10,
        },
      ],
    },
  ],
};
