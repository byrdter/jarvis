// Playbook: Claude Code
//
// Run:  node capture-runner.js claude-code
//
// Notes:
//   - Desktop surface is intentionally omitted (Claude Code Desktop is a
//     native app; capture those manually with Cmd+Shift+4 into
//     products/claude-code/surfaces/desktop/).
//   - CLI surface is best captured via asciinema, not Playwright.

export default {
  product: 'claude-code',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://claude.com/claude-code',
          wait: 2000,
        },
        {
          type: 'screenshot',
          name: 'hero-full',
          url: 'https://claude.com/claude-code',
          fullPage: true,
          wait: 2000,
        },
        {
          type: 'scroll-video',
          name: 'scroll-homepage',
          url: 'https://claude.com/claude-code',
          duration: 7,
        },
        {
          type: 'screenshot',
          name: 'docs-landing',
          url: 'https://docs.claude.com/en/docs/claude-code/overview',
          wait: 2000,
        },
      ],
    },
  ],
};
