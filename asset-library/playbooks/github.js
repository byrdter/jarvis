// Playbook: GitHub
//
// Run: node capture-runner.js github
//
// Public developer proof surfaces for agentic coding, workflows, issues,
// pull requests, CI, and open-source tool credibility.

export default {
  product: 'github',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://github.com/',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'repo-readme-scroll',
          url: 'https://github.com/langchain-ai/langgraph',
          duration: 10,
        },
        {
          type: 'screenshot',
          name: 'repo-readme',
          url: 'https://github.com/langchain-ai/langgraph',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'pull-requests-scroll',
          url: 'https://github.com/langchain-ai/langgraph/pulls',
          duration: 8,
        },
        {
          type: 'scroll-video',
          name: 'issues-scroll',
          url: 'https://github.com/langchain-ai/langgraph/issues',
          duration: 8,
        },
        {
          type: 'scroll-video',
          name: 'actions-scroll',
          url: 'https://github.com/langchain-ai/langgraph/actions',
          duration: 8,
        },
      ],
    },
  ],
};
