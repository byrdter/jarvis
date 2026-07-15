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

