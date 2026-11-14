#!/usr/bin/env bash
# JARVIS server, step 1: base hardening. Run as root on a fresh Ubuntu LTS (Hetzner).
# Idempotent: safe to re-run. Does NOT disable root/password SSH yet (02 does, after jarvis login is proven).
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

echo "== packages"
apt-get update -qq
apt-get -y -qq -o Dpkg::Options::=--force-confold upgrade
apt-get -y -qq install ufw unattended-upgrades tmux git curl jq unzip ca-certificates

echo "== automatic security updates"
dpkg-reconfigure -f noninteractive unattended-upgrades
systemctl enable --now unattended-upgrades

echo "== user jarvis"
if ! id jarvis >/dev/null 2>&1; then
  adduser --disabled-password --gecos "JARVIS" jarvis
fi
usermod -aG sudo jarvis
echo "jarvis ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-jarvis && chmod 440 /etc/sudoers.d/90-jarvis
install -d -m 700 -o jarvis -g jarvis /home/jarvis/.ssh
install -m 600 -o jarvis -g jarvis /root/.ssh/authorized_keys /home/jarvis/.ssh/authorized_keys
loginctl enable-linger jarvis   # user services keep running without a login session

echo "== swap (4 GB)"
if ! swapon --show | grep -q /swapfile; then
  fallocate -l 4G /swapfile && chmod 600 /swapfile && mkswap -q /swapfile && swapon /swapfile
  grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
fi
sysctl -q -w vm.swappiness=10
echo 'vm.swappiness=10' > /etc/sysctl.d/90-jarvis.conf

echo "== firewall (temporary: SSH open until Tailscale is up)"
ufw default deny incoming >/dev/null
ufw default allow outgoing >/dev/null
ufw allow 22/tcp >/dev/null
ufw --force enable >/dev/null
ufw status verbose | head -8

echo "== done"
