<template>
  <div class="auth-form">
    <h1 class="auth-form-title">{{ $t('auth.register') }}</h1>
    <form @submit.prevent="submit" class="auth-form-fields">
      <div class="field">
        <label for="reg-org" class="field-label required">{{ $t('auth.organisationName') }}</label>
        <input
          id="reg-org"
          v-model="organisationName"
          type="text"
          class="input"
          :class="{ error: !!error }"
          :placeholder="$t('auth.organisationName')"
          required
        />
      </div>
      <div class="field-row">
        <div class="field">
          <label for="reg-first" class="field-label">{{ $t('auth.firstName') }}</label>
          <input
            id="reg-first"
            v-model="form.first_name"
            type="text"
            class="input"
            :placeholder="$t('auth.firstName')"
          />
        </div>
        <div class="field">
          <label for="reg-last" class="field-label">{{ $t('auth.lastName') }}</label>
          <input
            id="reg-last"
            v-model="form.last_name"
            type="text"
            class="input"
            :placeholder="$t('auth.lastName')"
          />
        </div>
      </div>
      <div class="field">
        <label for="reg-email" class="field-label required">{{ $t('auth.email') }}</label>
        <input
          id="reg-email"
          v-model="form.email"
          type="email"
          class="input"
          :class="{ error: !!error }"
          :placeholder="$t('auth.email')"
          required
          autocomplete="email"
        />
      </div>
      <div class="field">
        <label for="reg-password" class="field-label required">{{ $t('auth.password') }}</label>
        <input
          id="reg-password"
          v-model="form.password"
          type="password"
          class="input"
          :class="{ error: !!error }"
          :placeholder="$t('auth.password')"
          required
          autocomplete="new-password"
        />
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <button type="submit" class="btn btn-primary auth-submit">
        {{ $t('auth.register') }}
      </button>
    </form>
    <p class="auth-footer">
      {{ $t('auth.hasAccount') }}
      <router-link to="/auth/login" class="auth-link">{{ $t('auth.signIn') }}</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const error = ref('')
const router = useRouter()
const authStore = useAuthStore()
const organisationName = ref('')
const form = reactive({
  first_name: '',
  last_name: '',
  email: '',
  password: '',
})

async function submit() {
  error.value = ''
  try {
    await authStore.register({
      organisationName: organisationName.value,
      email: form.email,
      password: form.password,
      first_name: form.first_name,
      last_name: form.last_name,
    })
    router.push('/')
  } catch (e) {
    const data = e.response?.data
    const msg = typeof data?.message === 'string' ? data.message : data?.message?.[0]
    if (e.response?.status === 403) {
      error.value = msg || 'Access forbidden (403). Check CORS/proxy or try without a stored token.'
    } else if (e.response?.status === 429) {
      error.value = msg || 'Too many registration attempts. Please wait before trying again.'
    } else {
      error.value = msg || e.message || 'Registration failed'
    }
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

.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
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

@media (max-width: 480px) {
  .field-row {
    grid-template-columns: 1fr;
  }
}
</style>
