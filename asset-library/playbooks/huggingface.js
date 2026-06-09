// Playbook: Hugging Face
//
// Run: node capture-runner.js huggingface
//
// Public model, dataset, Space, and blog surfaces for small-model,
// open-source, RAG, and AI ecosystem proof.

export default {
  product: 'huggingface',
  surfaces: [
    {
      name: 'web',
      shots: [
        {
          type: 'screenshot',
          name: 'hero',
          url: 'https://huggingface.co/',
          wait: 2500,
        },
        {
          type: 'scroll-video',
          name: 'models-scroll',
          url: 'https://huggingface.co/models',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'model-card-scroll',
          url: 'https://huggingface.co/Qwen/Qwen3-8B',
          duration: 12,
        },
        {
          type: 'scroll-video',
          name: 'datasets-scroll',
          url: 'https://huggingface.co/datasets',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'spaces-scroll',
          url: 'https://huggingface.co/spaces',
          duration: 10,
        },
        {
          type: 'scroll-video',
          name: 'blog-scroll',
          url: 'https://huggingface.co/blog',
          duration: 10,
        },
      ],
    },
  ],
};
