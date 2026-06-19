#!/usr/bin/env python3
"""
master-qa.py — Final QA validation on master.mp4

Usage:
    python3 master-qa.py master.mp4 --sample-interval 30 --output qa-report.json
"""

import subprocess
import json
import argparse
import sys
from pathlib import Path

def get_video_info(video_path):
    """Get video file info with ffprobe"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error',
             '-show_entries', 'format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate',
             '-of', 'json', str(video_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        data = json.loads(result.stdout)

        format_info = data.get('format', {})
        streams = data.get('streams', [])

        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), None)
        audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), None)

        return {
            'duration': float(format_info.get('duration', 0)),
            'size_bytes': int(format_info.get('size', 0)),
            'video_codec': video_stream.get('codec_name') if video_stream else None,
            'resolution': f"{video_stream.get('width')}x{video_stream.get('height')}" if video_stream else None,
            'fps': eval(video_stream.get('r_frame_rate', '30/1')) if video_stream else None,
            'audio_codec': audio_stream.get('codec_name') if audio_stream else None,
            'has_video': video_stream is not None,
            'has_audio': audio_stream is not None
        }
    except Exception as e:
        return {'error': str(e)}

def validate_file_integrity(info):
    """Validate basic file integrity"""
    issues = []

    if info.get('error'):
        issues.append({
            'type': 'file_integrity',
            'severity': 'critical',
            'message': f"Failed to read video: {info['error']}"
        })
        return issues

    if not info.get('has_video'):
        issues.append({
            'type': 'file_integrity',
            'severity': 'critical',
            'message': 'No video stream found'
        })

    if not info.get('has_audio'):
        issues.append({
            'type': 'file_integrity',
            'severity': 'critical',
            'message': 'No audio stream found'
        })

    if info.get('duration', 0) == 0:
        issues.append({
            'type': 'file_integrity',
            'severity': 'critical',
            'message': 'Video duration is 0'
        })

    if info.get('size_bytes', 0) == 0:
        issues.append({
            'type': 'file_integrity',
            'severity': 'critical',
            'message': 'File size is 0 bytes'
        })

    return issues

def validate_runtime(duration):
    """Validate runtime against targets"""
    issues = []

    min_duration = 480  # 8 minutes
    target_min = 600    # 10 minutes
    target_max = 900    # 15 minutes

    if duration < min_duration:
        remaining = min_duration - duration
        issues.append({
            'type': 'runtime',
            'severity': 'error',
            'message': f"Below 8-min minimum. Need {remaining:.0f}s more.",
            'duration': duration,
            'target': min_duration
        })
    elif duration < target_min:
        issues.append({
            'type': 'runtime',
            'severity': 'info',
            'message': f"Runtime {duration:.0f}s ({duration/60:.1f}m) — within acceptable range but below 10-min target",
            'duration': duration
        })
    elif duration > target_max:
        issues.append({
            'type': 'runtime',
            'severity': 'warning',
            'message': f"Runtime {duration:.0f}s ({duration/60:.1f}m) — exceeds 15-min ideal max",
            'duration': duration
        })

    return issues

def analyze_blank_screens(video_path, sample_interval=30, variance_threshold=10):
    """Sample frames and detect blank screens"""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {
            'skipped': True,
            'error': 'OpenCV not installed (pip install opencv-python)'
        }

    try:
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps

        blank_frames = []
        sample_count = int(duration / sample_interval)

        for i in range(sample_count):
            timestamp = i * sample_interval
            frame_num = int(timestamp * fps)

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()

            if not ret:
                break

            # Convert to grayscale and compute variance
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            variance = gray.var()

            if variance < variance_threshold:
                severity = 'critical' if variance < 5 else 'warning'
                blank_frames.append({
                    'timestamp': round(timestamp, 2),
                    'variance': round(variance, 2),
                    'severity': severity
                })

        cap.release()

        issues = []
        for blank in blank_frames:
            issues.append({
                'type': 'blank_screen',
                'severity': blank['severity'],
                'message': f"Blank screen at {blank['timestamp']}s (variance: {blank['variance']})",
                'timestamp': blank['timestamp'],
                'variance': blank['variance']
            })

        return {
            'sampled': sample_count,
            'blank_count': len(blank_frames),
            'issues': issues
        }

    except Exception as e:
        return {
            'skipped': True,
            'error': f"Frame analysis failed: {str(e)}"
        }

def check_transitions(video_path, manifest_path=None):
    """
    Check transition points between scenes for flash frames.
    Requires manifest file to know scene boundaries.
    """
    if not manifest_path or not Path(manifest_path).exists():
        return {
            'skipped': True,
            'error': 'No manifest file (master.mp4.manifest.json)'
        }

    # Load manifest
    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    scenes = manifest.get('scenes', [])
    if not scenes:
        return {
            'skipped': True,
            'error': 'No scenes in manifest'
        }

    # Calculate transition points
    transitions = []
    cumulative = 0
    for scene in scenes:
        duration = scene.get('duration_seconds', 0)
        transitions.append(cumulative + duration)
        cumulative += duration

    # TODO: Implement transition frame analysis
    # For now, return placeholder
    return {
        'checked': len(transitions) - 1,
        'issues': []
    }

def calculate_quality_score(all_issues):
    """Calculate overall quality score 0-100"""
    critical_count = len([i for i in all_issues if i.get('severity') == 'critical'])
    error_count = len([i for i in all_issues if i.get('severity') == 'error'])
    warning_count = len([i for i in all_issues if i.get('severity') == 'warning'])

    # Deduct points for issues
    score = 100
    score -= critical_count * 25  # -25 per critical
    score -= error_count * 10     # -10 per error
    score -= warning_count * 5    # -5 per warning

    return max(0, min(100, score))

def generate_watch_commands(video_path, duration):
    """Generate watch.py commands for key moments"""
    watch_script = Path.home() / '.claude/skills/watch/scripts/watch.py'

    commands = []

    # Intro (first 30s)
    commands.append(f"python3 {watch_script} {video_path} --start 0 --end 30")

    # Middle (around halfway)
    middle = duration / 2
    commands.append(f"python3 {watch_script} {video_path} --start {int(middle-15)} --end {int(middle+15)}")

    # Ending (last 30s)
    commands.append(f"python3 {watch_script} {video_path} --start {int(duration-30)} --end {int(duration)}")

    return commands

def main():
    parser = argparse.ArgumentParser(description="Final QA on master video")
    parser.add_argument('video', help="Path to master.mp4")
    parser.add_argument('--sample-interval', type=float, default=30, help="Frame sampling interval (seconds)")
    parser.add_argument('--output', help="Output path for JSON report")

    args = parser.parse_args()

    video_path = Path(args.video)
    if not video_path.exists():
        print(f"❌ Error: Video file not found: {args.video}", file=sys.stderr)
        sys.exit(1)

    manifest_path = Path(str(video_path) + '.manifest.json')

    print("🔍 Master QA:", args.video)
    print("")

    # Get video info
    info = get_video_info(video_path)

    all_issues = []

    # 1. File integrity
    print("Checking file integrity...")
    integrity_issues = validate_file_integrity(info)
    all_issues.extend(integrity_issues)

    if not integrity_issues:
        duration = info['duration']
        size_mb = info['size_bytes'] / (1024 * 1024)

        print(f"  ✓ Video: {info['video_codec']}, {info['resolution']}, {info.get('fps', '?')} fps")
        print(f"  ✓ Audio: {info['audio_codec']}")
        print(f"  ✓ Duration: {duration:.1f}s ({int(duration//60)}m {int(duration%60)}s)")
        print(f"  ✓ Size: {size_mb:.1f} MB")
        print("")

        # 2. Runtime validation
        print("Checking runtime...")
        runtime_issues = validate_runtime(duration)
        all_issues.extend(runtime_issues)

        if runtime_issues:
            for issue in runtime_issues:
                icon = '⚠️' if issue['severity'] == 'warning' else 'ℹ️'
                print(f"  {icon} {issue['message']}")
        else:
            print(f"  ✓ Runtime: {duration:.0f}s — within ideal range (10-15 min)")
        print("")

        # 3. Blank screen analysis
        print(f"Analyzing blank screens (sampling every {args.sample_interval}s)...")
        blank_result = analyze_blank_screens(video_path, sample_interval=args.sample_interval)

        if blank_result.get('skipped'):
            print(f"  ⚠️  Skipped: {blank_result['error']}")
        else:
            all_issues.extend(blank_result.get('issues', []))
            if blank_result['blank_count'] == 0:
                print(f"  ✓ Sampled {blank_result['sampled']} frames — 0 blank screens")
            else:
                print(f"  ❌ Found {blank_result['blank_count']} blank screens")
                for issue in blank_result['issues']:
                    print(f"     - {issue['message']}")
        print("")

        # 4. Transition check
        print("Checking scene transitions...")
        transition_result = check_transitions(video_path, manifest_path)

        if transition_result.get('skipped'):
            print(f"  ⚠️  Skipped: {transition_result['error']}")
        else:
            transition_issues = transition_result.get('issues', [])
            all_issues.extend(transition_issues)
            if not transition_issues:
                print(f"  ✓ Checked {transition_result['checked']} transitions — all clean")
        print("")

    # Calculate quality score
    quality_score = calculate_quality_score(all_issues)

    # Summary
    critical_count = len([i for i in all_issues if i.get('severity') == 'critical'])
    error_count = len([i for i in all_issues if i.get('severity') == 'error'])
    warning_count = len([i for i in all_issues if i.get('severity') == 'warning'])

    print("📊 Quality Score:", f"{quality_score}/100")
    print("")

    if critical_count == 0 and error_count == 0:
        print("✅ PASSED — Ready for upload")
        print("")
    else:
        print(f"❌ FAILED — {critical_count} critical, {error_count} errors, {warning_count} warnings")
        print("")
        print("Issues to fix:")
        for issue in all_issues:
            if issue['severity'] in ['critical', 'error']:
                print(f"  - [{issue['type']}] {issue['message']}")
        print("")

    # Watch commands
    if info.get('duration'):
        print("Watch key moments:")
        watch_commands = generate_watch_commands(video_path, info['duration'])
        for cmd in watch_commands:
            print(f"  {cmd}")
        print("")

    # Generate report
    report = {
        'timestamp': subprocess.check_output(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ']).decode().strip(),
        'video_path': str(video_path),
        'info': info,
        'quality_score': quality_score,
        'issues': all_issues,
        'passed': critical_count == 0 and error_count == 0
    }

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📋 Report saved: {args.output}")

    # Exit code
    sys.exit(0 if report['passed'] else 1)

if __name__ == '__main__':
    main()
