/**
 * TypeScript wrapper for YouTube transcript scraper
 *
 * Calls the Python script at:
 * /Users/terrybyrd/Library/CloudStorage/Dropbox/AI Strategist/YoutubeTranscript/youtube_channel_transcripts.py
 */

import { spawn } from 'child_process';
import { join } from 'path';
import { existsSync } from 'fs';

const SCRAPER_DIR = '/Users/terrybyrd/Library/CloudStorage/Dropbox/AI Strategist/YoutubeTranscript';
const SCRAPER_SCRIPT = join(SCRAPER_DIR, 'youtube_channel_transcripts.py');
const PYTHON_BIN = join(SCRAPER_DIR, 'venv', 'bin', 'python3');

export interface ScrapeOptions {
  channelUrl: string;
  numVideos?: number;
  skip?: number;
  outputFile?: string;
  audioFallback?: boolean;
  keepAudio?: boolean;
}

export interface ScrapeResult {
  success: boolean;
  outputFile: string;
  videosFound: number;
  transcriptsSuccess: number;
  errors: string[];
  stdout: string;
  stderr: string;
}

export class YouTubeScraper {

  /**
   * Scrape YouTube channel for video transcripts
   */
  async scrapeChannel(options: ScrapeOptions): Promise<ScrapeResult> {
    const {
      channelUrl,
      numVideos = 25,
      skip = 0,
      outputFile,
      audioFallback = false,
      keepAudio = false
    } = options;

    // Validate scraper exists
    if (!existsSync(SCRAPER_SCRIPT)) {
      throw new Error(`YouTube scraper not found at: ${SCRAPER_SCRIPT}`);
    }

    if (!existsSync(PYTHON_BIN)) {
      throw new Error(`Python venv not found at: ${PYTHON_BIN}. Run: cd "${SCRAPER_DIR}" && python3 -m venv venv && venv/bin/pip install -r requirements.txt`);
    }

    // Generate output filename if not provided
    const channelName = this.extractChannelName(channelUrl);
    const defaultOutput = join(SCRAPER_DIR, `${channelName}_transcripts.md`);
    const actualOutputFile = outputFile || defaultOutput;

    // Build command arguments
    const args = [
      SCRAPER_SCRIPT,
      channelUrl,
      '-n', numVideos.toString(),
      '-o', actualOutputFile
    ];

    if (skip > 0) {
      args.push('--skip', skip.toString());
    }

    if (audioFallback) {
      args.push('--audio-fallback');
    }

    if (keepAudio) {
      args.push('--keep-audio');
    }

    // Run scraper
    console.log(`🎥 Scraping YouTube channel: ${channelUrl}`);
    console.log(`   Videos: ${numVideos} (skip: ${skip})`);
    console.log(`   Output: ${actualOutputFile}`);

    const result = await this.runPythonScript(args);

    // Parse output for statistics
    const stats = this.parseScraperOutput(result.stdout);

    return {
      success: result.exitCode === 0,
      outputFile: actualOutputFile,
      videosFound: stats.videosFound,
      transcriptsSuccess: stats.transcriptsSuccess,
      errors: result.exitCode !== 0 ? [result.stderr] : [],
      stdout: result.stdout,
      stderr: result.stderr
    };
  }

  /**
   * Run Python script and capture output
   */
  private runPythonScript(args: string[]): Promise<{
    exitCode: number;
    stdout: string;
    stderr: string;
  }> {
    return new Promise((resolve) => {
      const process = spawn(PYTHON_BIN, args, {
        cwd: SCRAPER_DIR
      });

      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        const text = data.toString();
        stdout += text;
        console.log(text.trim());
      });

      process.stderr.on('data', (data) => {
        const text = data.toString();
        stderr += text;
        console.error(text.trim());
      });

      process.on('close', (code) => {
        resolve({
          exitCode: code || 0,
          stdout,
          stderr
        });
      });

      process.on('error', (error) => {
        resolve({
          exitCode: 1,
          stdout,
          stderr: error.message
        });
      });
    });
  }

  /**
   * Extract channel name from URL for default filename
   */
  private extractChannelName(url: string): string {
    // https://www.youtube.com/@ColeMedin -> cole_medin
    // https://www.youtube.com/c/ChannelName -> channel_name
    const match = url.match(/@([^\/\?]+)|\/c\/([^\/\?]+)|\/channel\/([^\/\?]+)/);

    if (match) {
      const name = match[1] || match[2] || match[3];
      return name.toLowerCase().replace(/\s+/g, '_');
    }

    return 'channel';
  }

  /**
   * Parse scraper output for statistics
   */
  private parseScraperOutput(output: string): {
    videosFound: number;
    transcriptsSuccess: number;
  } {
    const stats = {
      videosFound: 0,
      transcriptsSuccess: 0
    };

    // Parse: "Found 24 videos"
    const foundMatch = output.match(/Found (\d+) videos/);
    if (foundMatch) {
      stats.videosFound = parseInt(foundMatch[1]);
    }

    // Parse: "Successfully fetched transcripts for 20/24 videos"
    const successMatch = output.match(/Successfully fetched transcripts for (\d+)\/\d+ videos/);
    if (successMatch) {
      stats.transcriptsSuccess = parseInt(successMatch[1]);
    }

    return stats;
  }

  /**
   * Check if a channel has new videos since last check
   * (Compares first video ID with stored last video ID)
   */
  async checkForNewVideos(channelUrl: string, lastVideoId: string): Promise<{
    hasNew: boolean;
    newCount: number;
  }> {
    // Scrape just the first video to check
    const result = await this.scrapeChannel({
      channelUrl,
      numVideos: 1,
      outputFile: '/tmp/youtube_check.md'
    });

    if (!result.success) {
      return { hasNew: false, newCount: 0 };
    }

    // Parse the markdown to get first video ID
    const { readFileSync } = await import('fs');
    const content = readFileSync(result.outputFile, 'utf-8');

    const urlMatch = content.match(/\*\*URL:\*\*\s+https:\/\/www\.youtube\.com\/watch\?v=([^)\n]+)/);
    const firstVideoId = urlMatch ? urlMatch[1] : '';

    if (firstVideoId && firstVideoId !== lastVideoId) {
      // New video found! Estimate how many new videos
      // (Could scrape more to get exact count, but for now assume 1-5 new videos)
      return { hasNew: true, newCount: 1 };
    }

    return { hasNew: false, newCount: 0 };
  }
}

// Export singleton
export const youtubeScraper = new YouTubeScraper();
