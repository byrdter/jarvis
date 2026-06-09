// Playbook: AI Infrastructure
//
// Run: node capture-runner.js ai-infra
//
// Public deployment, observability, browser automation, and infrastructure
// surfaces for 2027 builder-roadmap videos.

export default {
  product: 'ai-infra',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'scroll-video',
          name: 'runpod-scroll',
          url: 'https://www.runpod.io/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'modal-scroll',
          url: 'https://modal.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'arize-scroll',
          url: 'https://arize.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'weave-scroll',
          url: 'https://wandb.ai/site/weave/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'browserbase-scroll',
          url: 'https://www.browserbase.com/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'vercel-ai-sdk-scroll',
          url: 'https://sdk.vercel.ai/docs',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'cloudflare-workers-ai-scroll',
          url: 'https://developers.cloudflare.com/workers-ai/',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'supabase-vector-scroll',
          url: 'https://supabase.com/docs/guides/ai',
          duration: 10,
        },
      ],
    },
  ],
};
