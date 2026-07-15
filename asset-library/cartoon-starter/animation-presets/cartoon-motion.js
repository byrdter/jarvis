export function popIn(gsap, target, options = {}) {
  const { duration = 0.42, scale = 0.82, ease = "back.out(1.8)" } = options;
  return gsap.fromTo(target, { autoAlpha: 0, scale }, { autoAlpha: 1, scale: 1, duration, ease });
}

export function gentleBob(gsap, target, options = {}) {
  const { y = -8, duration = 1.8 } = options;
  return gsap.to(target, { y, duration, repeat: -1, yoyo: true, ease: "sine.inOut" });
}

export function cameraPush(gsap, target, options = {}) {
  const { scale = 1.08, duration = 4.5 } = options;
  return gsap.to(target, { scale, duration, ease: "sine.inOut" });
}

export function quickShake(gsap, target, options = {}) {
  const { x = 8, duration = 0.08, repeat = 5 } = options;
  return gsap.to(target, { x, duration, repeat, yoyo: true, ease: "power1.inOut" });
}

export function slideLabel(gsap, target, options = {}) {
  const { x = -28, duration = 0.38 } = options;
  return gsap.fromTo(target, { autoAlpha: 0, x }, { autoAlpha: 1, x: 0, duration, ease: "power2.out" });
}

export function orbit(gsap, target, options = {}) {
  const { rotation = 360, duration = 6 } = options;
  return gsap.to(target, { rotation, transformOrigin: "50% 50%", duration, repeat: -1, ease: "none" });
}

export function drawPath(gsap, target, options = {}) {
  const { duration = 0.7 } = options;
  return gsap.fromTo(target, { strokeDasharray: 600, strokeDashoffset: 600 }, { strokeDashoffset: 0, duration, ease: "power2.out" });
}

export function softBlink(gsap, target, options = {}) {
  const { opacity = 0.45, duration = 0.9 } = options;
  return gsap.to(target, { opacity, duration, repeat: -1, yoyo: true, ease: "sine.inOut" });
}

export function squashPop(gsap, target, options = {}) {
  const { duration = 0.5, y = 12 } = options;
  const tl = gsap.timeline();
  tl.fromTo(target, { autoAlpha: 0, scaleX: 0.78, scaleY: 1.18, y }, { autoAlpha: 1, scaleX: 1.08, scaleY: 0.92, y: -4, duration: duration * 0.55, ease: "back.out(2)" });
  tl.to(target, { scaleX: 1, scaleY: 1, y: 0, duration: duration * 0.45, ease: "power2.out" });
  return tl;
}

export function attentionWiggle(gsap, target, options = {}) {
  const { rotation = 4, duration = 0.12, repeat = 7 } = options;
  return gsap.fromTo(target, { rotation: -rotation }, { rotation, transformOrigin: "50% 80%", duration, repeat, yoyo: true, ease: "sine.inOut" });
}

export function parallaxDrift(gsap, target, options = {}) {
  const { x = -28, y = 10, duration = 8 } = options;
  return gsap.to(target, { x, y, duration, repeat: -1, yoyo: true, ease: "sine.inOut" });
}

export function stampIn(gsap, target, options = {}) {
  const { duration = 0.36, rotation = -6 } = options;
  return gsap.fromTo(target, { autoAlpha: 0, scale: 1.42, rotation }, { autoAlpha: 1, scale: 1, rotation: 0, duration, ease: "back.out(2.4)" });
}

export function wipeReveal(gsap, target, options = {}) {
  const { duration = 0.62, xPercent = -102 } = options;
  return gsap.fromTo(target, { clipPath: `inset(0 0 0 ${Math.abs(xPercent)}%)` }, { clipPath: "inset(0 0 0 0%)", duration, ease: "power2.out" });
}

export function countPulse(gsap, target, options = {}) {
  const { scale = 1.16, duration = 0.22, repeat = 1 } = options;
  return gsap.to(target, { scale, transformOrigin: "50% 50%", duration, repeat, yoyo: true, ease: "power2.out" });
}

export function thoughtBubbleFloat(gsap, target, options = {}) {
  const { x = 8, y = -14, duration = 2.4 } = options;
  return gsap.to(target, { x, y, duration, repeat: -1, yoyo: true, ease: "sine.inOut" });
}

export function diagramBuild(gsap, targets, options = {}) {
  const { stagger = 0.12, duration = 0.36 } = options;
  return gsap.fromTo(targets, { autoAlpha: 0, y: 12, scale: 0.94 }, { autoAlpha: 1, y: 0, scale: 1, duration, stagger, ease: "power2.out" });
}
