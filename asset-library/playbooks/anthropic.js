// Playbook: Anthropic
//
// Run: node capture-runner.js anthropic
//
// Public Anthropic product, Claude Code, docs, news, and research surfaces.

export default {
  product: 'anthropic',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://www.anthropic.com/',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'homepage-scroll',
          url: 'https://www.anthropic.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'claude-code-docs-scroll',
          url: 'https://docs.claude.com/en/docs/claude-code/overview',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'docs-scroll',
          url: 'https://docs.claude.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'news-scroll',
          url: 'https://www.anthropic.com/news',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'research-scroll',
          url: 'https://www.anthropic.com/research',
          duration: 10,
        },
      ],
    },
  ],
};
