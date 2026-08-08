// MID-SCENE MOUNT PROBE — the one thing `hyperframes check` structurally cannot catch.
//
// The demo mounts at sceneStart:0, where nothing is in the past, so it never exercises the
// branch that opens a mid-video scene with its history already on screen. On 2026-08-04 that
// branch was broken (tl.set at position 0 never ticks when the playhead is already at 0) and
// every scene after S01 would have rendered a blank panel. The demo passed check and render
// anyway. This probe is the check that would have caught it.
//
// HOW TO RUN: load demo/index.html in a browser, paste this into the console.
// Expect PASS on all three scenes. Re-run after ANY edit to spine-ledger.html.

(function () {
  var REAL = {
    ledger: [
      { label: 'PAID', value: '$1,000',  at: 0.12 },
      { label: 'USED', value: '$13,753', at: 6.15 },
      { label: 'GAP',  value: '$12,753', at: 35.52, emphasis: true }
    ],
    ghostsIn: 12.0,
    rows: [
      { q: 'WHERE DOES IT GO?',     open: 162.3,
        answers: [{ text: 'LONG SESSIONS · 10% = 90%', at: 224.1 }] },
      { q: 'WHO ABSORBS IT?',       open: 262.1,
        answers: [{ text: 'UNVERIFIABLE FROM OUTSIDE', at: 282.0, tone: 'closed' }] },
      { q: 'DOES IT CLOSE ITSELF?', open: 306.8,
        answers: [{ text: 'YES — PRICE FELL 3×', at: 327.8, tone: 'provisional' },
                  { text: 'NO — THE FALL STOPPED',    at: 409.0 }] },
      { q: 'WHAT MOVES FIRST?',     open: 476.8,
        answers: [{ text: 'THE LONG SESSIONS FIRST', at: 574.7, verdict: true }] }
    ]
  };

  function op(id) {
    var e = document.getElementById(id);
    return e ? Math.round(getComputedStyle(e).opacity * 100) / 100 : null;
  }

  function probe(sceneStart) {
    var t = gsap.timeline({ paused: true });
    var o = { sceneStart: sceneStart };
    for (var k in REAL) o[k] = REAL[k];
    mountLedger(t, o);
    t.seek(0);
    var counters = [];
    for (var k2 = 0; k2 <= 4; k2++) counters.push(op('lg-n-' + k2));
    return {
      panel:    op('lg'),
      gapValue: op('lg-lv-2'),
      q:        [op('lg-q-0'), op('lg-q-1'), op('lg-q-2'), op('lg-q-3')],
      a:        [op('lg-a-0-0'), op('lg-a-1-0'), op('lg-a-2-0'), op('lg-a-2-1'), op('lg-a-3-0')],
      ghostQ3:  op('lg-gq-3'),
      strike:   Math.round(gsap.getProperty('#lg-st-2-0', 'scaleX') * 100) / 100,
      visibleCounter: counters.reduce(function (acc, v, i) {
        return v > 0.5 ? i : acc; }, -1)
    };
  }

  // scene -> what the frame MUST already show at its t=0
  var CASES = [
    { name: 'S01 @0     (nothing past)', start: 0,
      want: { panel: 0, q: [0, 0, 0, 0], a: [0, 0, 0, 0, 0], strike: 0, visibleCounter: -1 } },
    { name: 'S07 @428.9 (rows 1-3 done)', start: 428.9,
      want: { panel: 1, gapValue: 1, q: [1, 1, 1, 0], a: [1, 1, 0.5, 1, 0],
              ghostQ3: 1, strike: 1, visibleCounter: 3 } },
    { name: 'S10 @574.64 (verdict pending)', start: 574.64,
      want: { panel: 1, gapValue: 1, q: [1, 1, 1, 1], a: [1, 1, 0.5, 1, 0],
              strike: 1, visibleCounter: 3 } }
  ];

  var allPass = true;
  CASES.forEach(function (c) {
    var got = probe(c.start), bad = [];
    Object.keys(c.want).forEach(function (k) {
      var w = JSON.stringify(c.want[k]), g = JSON.stringify(got[k]);
      if (w !== g) bad.push(k + ': want ' + w + ' got ' + g);
    });
    if (bad.length) allPass = false;
    console.log((bad.length ? '✗ FAIL  ' : '✓ PASS  ') + c.name +
                (bad.length ? '\n         ' + bad.join('\n         ') : ''));
  });
  console.log(allPass ? '\nALL PASS — mid-scene mount is correct.'
                      : '\nFAILED — scenes after S01 will not open in the right state.');
  return allPass;
})();
