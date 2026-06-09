// Playbook: MCP Registry / Ecosystem
//
// Run: node capture-runner.js mcp-registry
//
// Public MCP ecosystem surfaces for tool-server and tool-registry visuals.

export default {
  product: 'mcp-registry',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'scroll-video',
          name: 'modelcontextprotocol-scroll',
          url: 'https://modelcontextprotocol.io/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'mcp-docs-scroll',
          url: 'https://modelcontextprotocol.io/docs',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'mcp-github-scroll',
          url: 'https://github.com/modelcontextprotocol',
          duration: 10,
        },
      ],
    },
  ],
};
