#!/usr/bin/env python3
"""
scene-validator.py — Validate HyperFrames scenes for QA issues

Usage:
    python3 scene-validator.py <project-dir>                # Lint + structure
    python3 scene-validator.py <project-dir> --frames       # Add frame analysis
    python3 scene-validator.py <project-dir> --fix          # Auto-fix safe issues
    python3 scene-validator.py <project-dir> --json         # Machine-readable output
"""

import subprocess
import json
import argparse
import sys
from pathlib import Path

def find_scenes(project_dir):
    """Find all scene directories in project"""
    scenes_dir = Path(project_dir) / 'scenes'
    if not scenes_dir.exists():
        return []

    return sorted([d for d in scenes_dir.iterdir() if d.is_dir() and not d.name.startswith('.')])

def run_hyperframes_lint(scene_dir):
    """Run npx hyperframes lint on scene"""
    try:
        result = subprocess.run(
            ['npx', 'hyperframes', 'lint'],
            cwd=scene_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            'passed': result.returncode == 0,
            'output': result.stdout + result.stderr
        }
    except Exception as e:
        return {
            'passed': False,
            'output': f"Error running lint: {str(e)}"
        }

def validate_duration(scene_dir):
    """Validate rendered duration matches declared duration"""
    # Load hyperframes.json
    hf_json_path = scene_dir / 'hyperframes.json'
    if not hf_json_path.exists():
        return {
            'passed': False,
            'error': 'Missing hyperframes.json'
        }

    with open(hf_json_path, 'r') as f:
        hf_data = json.load(f)

    declared_duration = hf_data.get('compositions', [{}])[0].get('duration')
    if not declared_duration:
        return {
            'passed': False,
            'error': 'No duration in hyperframes.json'
        }

    # Find most recent render
    renders_dir = scene_dir / 'renders'
    if not renders_dir.exists():
        return {
            'passed': False,
            'error': 'No renders/ directory'
        }

    # Check for LOCKED file
    locked_file = renders_dir / 'LOCKED'
    if locked_file.exists():
        with open(locked_file, 'r') as f:
            render_name = f.read().strip()
        render_path = renders_dir / render_name
    else:
        # Find most recent .mp4
        mp4_files = sorted(renders_dir.glob('*.mp4'), key=lambda p: p.stat().st_mtime, reverse=True)
        if not mp4_files:
            return {
                'passed': False,
                'error': 'No rendered .mp4 files found'
            }
        render_path = mp4_files[0]

    # Get actual duration with ffprobe
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', str(render_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        actual_duration = float(result.stdout.strip())
    except Exception as e:
        return {
            'passed': False,
            'error': f"Failed to get duration: {str(e)}"
        }

    # Check tolerance ±0.5s
    diff = abs(actual_duration - declared_duration)
    tolerance = 0.5

    return {
        'passed': diff <= tolerance,
        'declared': declared_duration,
        'actual': actual_duration,
        'diff': diff,
        'render_path': str(render_path.name)
    }

def check_audio_stream(render_path):
    """Check if rendered video has audio stream"""
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'a:0',
             '-show_entries', 'stream=codec_name,duration',
             '-of', 'json', str(render_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        data = json.loads(result.stdout)
        streams = data.get('streams', [])

        if not streams:
            return {
                'passed': False,
                'error': 'No audio stream found'
            }

        return {
            'passed': True,
            'codec': streams[0].get('codec_name'),
            'duration': streams[0].get('duration')
        }
    except Exception as e:
        return {
            'passed': False,
            'error': f"Failed to check audio: {str(e)}"
        }

def analyze_frames(render_path, sample_interval=1.0, variance_threshold=10):
    """
    Analyze frames for blank screens.
    Requires OpenCV (pip install opencv-python).
    """
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {
            'skipped': True,
            'error': 'OpenCV not installed (pip install opencv-python)'
        }

    try:
        cap = cv2.VideoCapture(str(render_path))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        blank_frames = []

        for i in range(0, frame_count, int(fps * sample_interval)):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()

            if not ret:
                break

            # Convert to grayscale and compute variance
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            variance = gray.var()

            timestamp = i / fps

            if variance < variance_threshold:
                severity = 'critical' if variance < 5 else 'warning'
                blank_frames.append({
                    'timestamp': round(timestamp, 2),
                    'variance': round(variance, 2),
                    'severity': severity
                })

        cap.release()

        return {
            'passed': len(blank_frames) == 0,
            'blank_count': len(blank_frames),
            'blank_frames': blank_frames
        }

    except Exception as e:
        return {
            'skipped': True,
            'error': f"Frame analysis failed: {str(e)}"
        }

def validate_scene(scene_dir, check_frames=False):
    """Run all validations on a scene"""
    scene_name = scene_dir.name
    issues = []

    # 1. Lint check
    lint_result = run_hyperframes_lint(scene_dir)
    if not lint_result['passed']:
        issues.append({
            'type': 'lint',
            'severity': 'error',
            'message': 'HyperFrames lint failed',
            'details': lint_result['output']
        })

    # 2. Duration validation
    duration_result = validate_duration(scene_dir)
    if not duration_result['passed']:
        issues.append({
            'type': 'duration',
            'severity': 'error',
            'message': duration_result.get('error', 'Duration mismatch'),
            'details': duration_result
        })
    elif duration_result.get('diff', 0) > 0.1:
        issues.append({
            'type': 'duration',
            'severity': 'warning',
            'message': f"Duration drift: {duration_result['diff']:.2f}s",
            'details': duration_result
        })

    # 3. Audio stream check
    if duration_result.get('render_path'):
        render_path = scene_dir / 'renders' / duration_result['render_path']
        audio_result = check_audio_stream(render_path)

        if not audio_result['passed']:
            issues.append({
                'type': 'audio',
                'severity': 'critical',
                'message': audio_result.get('error', 'Audio stream missing'),
                'details': audio_result
            })

        # 4. Frame analysis (if requested)
        if check_frames:
            frame_result = analyze_frames(render_path)

            if frame_result.get('skipped'):
                issues.append({
                    'type': 'frames',
                    'severity': 'info',
                    'message': 'Frame analysis skipped',
                    'details': frame_result.get('error')
                })
            elif not frame_result['passed']:
                for blank in frame_result['blank_frames']:
                    issues.append({
                        'type': 'blank_screen',
                        'severity': blank['severity'],
                        'message': f"Blank screen at {blank['timestamp']}s (variance: {blank['variance']})",
                        'timestamp': blank['timestamp'],
                        'variance': blank['variance']
                    })

    return {
        'scene': scene_name,
        'passed': len([i for i in issues if i['severity'] in ['error', 'critical']]) == 0,
        'issues': issues
    }

def format_output(results, output_json=False):
    """Format validation results"""
    if output_json:
        print(json.dumps(results, indent=2))
        return

    # Text output
    print("🔍 Scene Validator")
    print("")

    total_scenes = len(results)
    passed_scenes = len([r for r in results if r['passed']])
    failed_scenes = total_scenes - passed_scenes

    # Summary
    critical_issues = sum(len([i for i in r['issues'] if i['severity'] == 'critical']) for r in results)
    error_issues = sum(len([i for i in r['issues'] if i['severity'] == 'error']) for r in results)
    warning_issues = sum(len([i for i in r['issues'] if i['severity'] == 'warning']) for r in results)

    # Per-scene results
    for result in results:
        scene_issues = result['issues']
        critical_count = len([i for i in scene_issues if i['severity'] == 'critical'])
        error_count = len([i for i in scene_issues if i['severity'] == 'error'])

        if result['passed']:
            print(f"  ✓ {result['scene']}")
        else:
            print(f"  ❌ {result['scene']} — {critical_count + error_count} issue(s)")

            for issue in scene_issues:
                if issue['severity'] in ['critical', 'error']:
                    icon = '❌' if issue['severity'] == 'critical' else '⚠️'
                    print(f"     {icon} [{issue['type']}] {issue['message']}")

    print("")
    print(f"📊 Summary:")
    print(f"  - Total scenes: {total_scenes}")
    print(f"  - Passed: {passed_scenes}")
    print(f"  - Failed: {failed_scenes}")
    print(f"  - Issues: {critical_issues} critical, {error_issues} errors, {warning_issues} warnings")
    print("")

    if failed_scenes > 0:
        print("❌ FAILED — Fix issues before proceeding")
        return 1
    else:
        print("✅ PASSED — All scenes valid")
        return 0

def main():
    parser = argparse.ArgumentParser(description="Validate HyperFrames scenes")
    parser.add_argument('project_dir', help="Project directory containing scenes/")
    parser.add_argument('--frames', action='store_true', help="Run frame analysis (requires OpenCV)")
    parser.add_argument('--fix', action='store_true', help="Auto-fix safe issues (not implemented)")
    parser.add_argument('--json', action='store_true', help="Output JSON format")

    args = parser.parse_args()

    project_path = Path(args.project_dir)
    if not project_path.exists():
        print(f"❌ Error: Project directory not found: {args.project_dir}", file=sys.stderr)
        sys.exit(1)

    # Find scenes
    scenes = find_scenes(project_path)
    if not scenes:
        print(f"❌ Error: No scenes found in {project_path}/scenes/", file=sys.stderr)
        sys.exit(1)

    # Validate each scene
    results = []
    for scene_dir in scenes:
        result = validate_scene(scene_dir, check_frames=args.frames)
        results.append(result)

    # Output results
    exit_code = format_output(results, output_json=args.json)
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
