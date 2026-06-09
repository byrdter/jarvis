// Playbook: LangChain / LangGraph / LangSmith
//
// Run: node capture-runner.js langchain
//
// Public agent workflow, graph orchestration, tracing, and deployment surfaces.

export default {
  product: 'langchain',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://www.langchain.com/',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'homepage-scroll',
          url: 'https://www.langchain.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'langgraph-docs-scroll',
          url: 'https://langchain-ai.github.io/langgraph/',
          duration: 12,
        },
        {
          type: 'scroll-video',
          name: 'langsmith-scroll',
          url: 'https://www.langchain.com/langsmith',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'docs-scroll',
          url: 'https://docs.langchain.com/',
          duration: 10,
        },
      ],
    },
  ],
};
