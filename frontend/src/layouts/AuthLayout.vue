<template>
  <div class="auth-layout">
    <div class="auth-bg">
      <div class="auth-pattern" aria-hidden="true" />
    </div>
    <div class="auth-card">
      <div class="auth-brand">
        <span class="auth-logo">Faimous</span>
        <p class="auth-tagline">{{ $t('dashboard.title') }}</p>
      </div>
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-6);
  position: relative;
  overflow: hidden;
}

.auth-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, var(--color-sidebar) 0%, #1e293b 50%, #334155 100%);
}

.auth-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.04;
  background-image: radial-gradient(circle at 1px 1px, white 1px, transparent 0);
  background-size: 32px 32px;
}

.auth-card {
  position: relative;
  width: 100%;
  max-width: 420px;
  background: var(--color-surface);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  padding: var(--space-8);
  border: 1px solid var(--color-border);
}

.auth-brand {
  text-align: center;
  margin-bottom: var(--space-8);
}

.auth-logo {
  display: block;
  font-size: var(--text-2xl);
  font-weight: var(--font-bold);
  color: var(--color-primary);
  letter-spacing: -0.02em;
}

.auth-tagline {
  margin: var(--space-1) 0 0 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
</style>
