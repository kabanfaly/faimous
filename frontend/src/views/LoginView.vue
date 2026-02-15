<template>
  <div class="auth-form">
    <h1 class="auth-form-title">{{ $t('auth.login') }}</h1>
    <form @submit.prevent="submit" class="auth-form-fields">
      <div class="field">
        <label for="login-email" class="field-label required">{{ $t('auth.email') }}</label>
        <input
          id="login-email"
          v-model="email"
          type="email"
          class="input"
          :class="{ error: !!error }"
          :placeholder="$t('auth.email')"
          required
          autocomplete="email"
        />
      </div>
      <div class="field">
        <label for="login-password" class="field-label required">{{ $t('auth.password') }}</label>
        <input
          id="login-password"
          v-model="password"
          type="password"
          class="input"
          :class="{ error: !!error }"
          :placeholder="$t('auth.password')"
          required
          autocomplete="current-password"
        />
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <button type="submit" class="btn btn-primary auth-submit">
        {{ $t('auth.login') }}
      </button>
    </form>
    <p class="auth-footer">
      {{ $t('auth.noAccount') }}
      <router-link to="/auth/register" class="auth-link">{{ $t('auth.signUp') }}</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const error = ref('')
const router = useRouter()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')

async function submit() {
  error.value = ''
  try {
    await authStore.login(email.value, password.value)
    router.push(router.currentRoute.value.query.redirect || '/')
  } catch (e) {
    const msg = e.response?.data?.message || e.message
    error.value = msg || (e.response?.status === 403 ? 'Account is not active.' : 'Login failed.')
  }
}
</script>

<style scoped>
.auth-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

.auth-form-title {
  margin: 0;
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text);
}

.auth-form-fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.field-label {
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text);
}

.auth-submit {
  width: 100%;
  margin-top: var(--space-2);
  padding: var(--space-4);
}

.auth-footer {
  margin: 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  text-align: center;
}

.auth-link {
  color: var(--color-primary);
  font-weight: var(--font-medium);
  text-decoration: none;
  margin-left: var(--space-1);
}

.auth-link:hover {
  text-decoration: underline;
}
</style>
