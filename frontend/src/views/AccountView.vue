<template>
  <div class="page account-page">
    <PageHeader>
      {{ $t('account.title') }}
      <template #subtitle>{{ auth.organisation?.name ?? auth.user?.email }}</template>
    </PageHeader>

    <div class="account-grid">
      <!-- Profile card -->
      <section class="card card-body account-card">
        <div class="account-card-header">
          <h2 class="section-title">{{ $t('account.profile') }}</h2>
          <button
            v-if="!editingProfile"
            type="button"
            class="btn btn-ghost btn-sm"
            @click="startEditProfile"
          >
            {{ $t('account.editProfile') }}
          </button>
          <div v-else class="form-actions">
            <button type="button" class="btn btn-ghost btn-sm" @click="cancelEditProfile">
              {{ $t('common.cancel') }}
            </button>
            <button type="button" class="btn btn-primary btn-sm" :disabled="profileSaving" @click="saveProfile">
              {{ $t('common.save') }}
            </button>
          </div>
        </div>

        <div v-if="profileSuccess" class="account-message account-message--success" role="status">
          {{ $t('account.profileUpdated') }}
        </div>
        <div v-if="profileError" class="account-message account-message--error" role="alert">
          {{ profileError }}
        </div>

        <template v-if="!editingProfile">
          <dl class="account-dl">
            <div v-if="auth.organisation?.name" class="account-dl-row">
              <dt>{{ $t('account.organisation') }}</dt>
              <dd>{{ auth.organisation.name }}</dd>
            </div>
            <div class="account-dl-row">
              <dt>{{ $t('account.firstName') }}</dt>
              <dd>{{ auth.user?.first_name ?? '—' }}</dd>
            </div>
            <div class="account-dl-row">
              <dt>{{ $t('account.lastName') }}</dt>
              <dd>{{ auth.user?.last_name ?? '—' }}</dd>
            </div>
            <div class="account-dl-row">
              <dt>{{ $t('account.email') }}</dt>
              <dd>{{ auth.user?.email ?? '—' }}</dd>
            </div>
          </dl>
        </template>
        <form v-else class="form-fields account-form" @submit.prevent="saveProfile">
          <div class="form-group">
            <label for="account-first-name">{{ $t('account.firstName') }}</label>
            <input
              id="account-first-name"
              v-model="profileForm.first_name"
              type="text"
              class="input"
              :placeholder="$t('account.firstName')"
            />
          </div>
          <div class="form-group">
            <label for="account-last-name">{{ $t('account.lastName') }}</label>
            <input
              id="account-last-name"
              v-model="profileForm.last_name"
              type="text"
              class="input"
              :placeholder="$t('account.lastName')"
            />
          </div>
          <div class="form-group">
            <label for="account-email" class="required">{{ $t('account.email') }}</label>
            <input
              id="account-email"
              v-model="profileForm.email"
              type="email"
              class="input"
              :placeholder="$t('auth.email')"
              required
            />
          </div>
        </form>
      </section>

      <!-- Change password card -->
      <section class="card card-body account-card">
        <h2 class="section-title">{{ $t('account.changePassword') }}</h2>

        <div v-if="passwordSuccess" class="account-message account-message--success" role="status">
          {{ $t('account.passwordUpdated') }}
        </div>
        <div v-if="passwordError" class="account-message account-message--error" role="alert">
          {{ passwordError }}
        </div>

        <form class="form-fields account-form" @submit.prevent="submitPassword">
          <div class="form-group">
            <label for="account-current-password" class="required">{{ $t('account.currentPassword') }}</label>
            <input
              id="account-current-password"
              v-model="passwordForm.current_password"
              type="password"
              class="input"
              :placeholder="$t('account.currentPassword')"
              autocomplete="current-password"
            />
          </div>
          <div class="form-group">
            <label for="account-new-password" class="required">{{ $t('account.newPassword') }}</label>
            <input
              id="account-new-password"
              v-model="passwordForm.new_password"
              type="password"
              class="input"
              :placeholder="$t('account.newPassword')"
              autocomplete="new-password"
              minlength="6"
            />
          </div>
          <div class="form-group">
            <label for="account-confirm-password" class="required">{{ $t('account.confirmPassword') }}</label>
            <input
              id="account-confirm-password"
              v-model="passwordForm.confirm_password"
              type="password"
              class="input"
              :placeholder="$t('account.confirmPassword')"
              autocomplete="new-password"
              :class="{ error: passwordForm.confirm_password && passwordMismatch }"
            />
            <p v-if="passwordForm.confirm_password && passwordMismatch" class="account-field-error">
              {{ $t('account.passwordMismatch') }}
            </p>
          </div>
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" :disabled="passwordSaving || !canSubmitPassword">
              {{ passwordSaving ? $t('common.loading') : $t('account.changePassword') }}
            </button>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '../store/auth'
import PageHeader from '../components/PageHeader.vue'

const auth = useAuthStore()

const editingProfile = ref(false)
const profileSaving = ref(false)
const profileSuccess = ref('')
const profileError = ref('')
const profileForm = ref({ first_name: '', last_name: '', email: '' })

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})
const passwordSaving = ref(false)
const passwordSuccess = ref('')
const passwordError = ref('')

const passwordMismatch = computed(
  () =>
    passwordForm.value.new_password &&
    passwordForm.value.confirm_password &&
    passwordForm.value.new_password !== passwordForm.value.confirm_password
)

const canSubmitPassword = computed(() => {
  const { current_password, new_password, confirm_password } = passwordForm.value
  return (
    current_password &&
    new_password &&
    new_password.length >= 6 &&
    confirm_password &&
    new_password === confirm_password
  )
})

function startEditProfile() {
  profileForm.value = {
    first_name: auth.user?.first_name ?? '',
    last_name: auth.user?.last_name ?? '',
    email: auth.user?.email ?? '',
  }
  profileSuccess.value = ''
  profileError.value = ''
  editingProfile.value = true
}

function cancelEditProfile() {
  editingProfile.value = false
  profileError.value = ''
}

async function saveProfile() {
  profileError.value = ''
  profileSaving.value = true
  try {
    await auth.updateProfile(profileForm.value)
    profileSuccess.value = 'ok'
    editingProfile.value = false
    setTimeout(() => { profileSuccess.value = '' }, 3000)
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data?.errors?.email?.[0] || err.message
    profileError.value = msg
  } finally {
    profileSaving.value = false
  }
}

async function submitPassword() {
  if (!canSubmitPassword.value || passwordSaving.value) return
  passwordError.value = ''
  passwordSuccess.value = ''
  passwordSaving.value = true
  try {
    await auth.changePassword(passwordForm.value.current_password, passwordForm.value.new_password)
    passwordSuccess.value = 'ok'
    passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
    setTimeout(() => { passwordSuccess.value = '' }, 4000)
  } catch (err) {
    passwordError.value =
      err.response?.data?.message || err.response?.data?.errors?.current_password?.[0] || err.message
  } finally {
    passwordSaving.value = false
  }
}

watch(passwordMismatch, () => {
  if (passwordMismatch.value) passwordError.value = ''
})
watch(
  () => passwordForm.value.confirm_password,
  () => {
    if (passwordError.value) passwordError.value = ''
  }
)
</script>

<style scoped>
.account-page {
  max-width: 56rem;
}

.account-grid {
  display: grid;
  gap: var(--space-8);
  grid-template-columns: 1fr 1fr;
}

@media (max-width: 768px) {
  .account-grid {
    grid-template-columns: 1fr;
  }
}

.account-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.account-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-3);
}

.account-card-header .section-title {
  margin: 0;
}

.account-dl {
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.account-dl-row {
  display: grid;
  grid-template-columns: 10rem 1fr;
  gap: var(--space-4);
  align-items: baseline;
}

.account-dl-row dt {
  margin: 0;
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-muted);
}

.account-dl-row dd {
  margin: 0;
  font-size: var(--text-base);
  color: var(--color-text);
}

.account-form {
  max-width: 100%;
}

.account-message {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
}

.account-message--success {
  color: #047857;
  background: #d1fae5;
}

.account-message--error {
  color: var(--color-error);
  background: var(--color-error-bg);
}

.account-field-error {
  margin: var(--space-1) 0 0;
  font-size: var(--text-sm);
  color: var(--color-error);
}
</style>
