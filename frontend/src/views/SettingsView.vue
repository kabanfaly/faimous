<template>
  <div class="page">
    <PageHeader>
      {{ $t('settings.title') }}
      <template #subtitle>{{ $t('settings.subtitle') }}</template>
    </PageHeader>

    <section v-if="!isAdmin" class="card card-body">
      <p class="settings-empty">{{ $t('settings.noAccess') }}</p>
    </section>

    <section v-if="isAdmin" class="card card-body">
      <h2 class="section-title">{{ $t('settings.organisation') }}</h2>
      <div v-if="orgSuccess" class="settings-message settings-message--success" role="status">
        {{ $t('settings.organisationUpdated') }}
      </div>
      <div v-if="orgError" class="settings-message settings-message--error" role="alert">
        {{ orgError }}
      </div>
      <form class="form-fields" style="max-width: 24rem;" @submit.prevent="submitOrganisation">
        <div class="form-group">
          <label class="required">{{ $t('settings.organisationName') }}</label>
          <input v-model="orgForm.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('settings.currencyDefault') }}</label>
          <select v-model="orgForm.currency_default" class="input">
            <option value="">{{ $t('common.selectCurrency') }}</option>
            <option v-for="c in currencies" :key="c.code" :value="c.code">
              {{ c.symbol }} — {{ c.name }} ({{ c.code }})
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('settings.languageDefault') }}</label>
          <input v-model="orgForm.language_default" type="text" class="input" maxlength="10" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary" :disabled="orgSaving">
            {{ $t('common.save') }}
          </button>
        </div>
      </form>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import PageHeader from '../components/PageHeader.vue'
import { useAuthStore } from '../store/auth'
import { getCurrencies } from '../api/currencies'

const auth = useAuthStore()
const currencies = ref([])

const isAdmin = computed(() => {
  const role = auth.user?.role
  return role === 'owner' || role === 'admin'
})

const orgForm = ref({
  name: '',
  currency_default: '',
  language_default: '',
})
const orgSaving = ref(false)
const orgSuccess = ref(false)
const orgError = ref('')

function resetOrgForm() {
  const o = auth.organisation
  orgForm.value = {
    name: o?.name ?? '',
    currency_default: o?.currency_default ?? '',
    language_default: o?.language_default ?? '',
  }
}

watch(
  () => auth.organisation,
  (o) => {
    if (o) resetOrgForm()
  },
  { immediate: true }
)

async function loadCurrencies() {
  try {
    currencies.value = await getCurrencies()
  } catch (e) {
    console.error(e)
  }
}

watch(isAdmin, (admin) => {
  if (admin && currencies.value.length === 0) {
    loadCurrencies()
  }
}, { immediate: true })

async function submitOrganisation() {
  orgError.value = ''
  orgSuccess.value = false
  orgSaving.value = true
  try {
    await auth.updateOrganisation({
      name: orgForm.value.name,
      currency_default: orgForm.value.currency_default || undefined,
      language_default: orgForm.value.language_default || undefined,
    })
    orgSuccess.value = true
    setTimeout(() => { orgSuccess.value = false }, 3000)
  } catch (e) {
    orgError.value = e.response?.data?.message ?? e.message ?? 'Failed to update organisation'
  } finally {
    orgSaving.value = false
  }
}
</script>

<style scoped>
.settings-message {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-4);
}
.settings-message--success {
  color: #047857;
  background: #d1fae5;
}
.settings-message--error {
  color: var(--color-error);
  background: var(--color-error-bg);
}

.settings-empty {
  margin: 0;
  color: var(--text-muted, #6b7280);
}
</style>
