<template>
  <div class="page">
    <PageHeader>
      {{ $t('financing.title') }}
      <template #subtitle>{{ $t('financing.contributions') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('financing.contributions') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddShareholder">{{ $t('common.add') }} {{ $t('shareholders.title') }}</button>
      </div>
      <PaginatedTable
        :items="shareholders"
        :columns="shareholderColumns"
        :loading="loading"
        :empty-text="$t('financing.emptyShareholders')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditShareholder(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteShareholder(item)" />
        </template>
      </PaginatedTable>
    </section>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('financing.contributionsList') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddContribution">{{ $t('common.add') }} {{ $t('financing.contribution') }}</button>
      </div>
      <p v-if="contributions.length" class="financing-total">
        {{ $t('common.total') }}: <strong>{{ formatAmount(contributionsTotal) }}</strong>
      </p>
      <PaginatedTable
        :items="contributions"
        :columns="contributionColumns"
        :loading="loading"
        :empty-text="$t('financing.emptyContributions')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditContribution(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteContribution(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="shareholderModalOpen" :title="shareholderModalTitle">
      <form @submit.prevent="submitShareholder" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('shareholders.firstName') }}</label>
          <input v-model="shareholderForm.first_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('shareholders.lastName') }}</label>
          <input v-model="shareholderForm.last_name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('shareholders.phone') }}</label>
          <input v-model="shareholderForm.phone" type="text" class="input" />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('shareholders.email') }}</label>
          <input v-model="shareholderForm.email" type="email" class="input" required />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeShareholderModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="contributionModalOpen" :title="contributionModalTitle">
      <form @submit.prevent="submitContribution" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="contributionForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('financing.shareholder') }}</label>
          <select v-model="contributionForm.shareholder_id" class="input">
            <option value="">{{ $t('common.selectShareholder') }}</option>
            <option v-for="s in shareholders" :key="s.id" :value="s.id">{{ s.first_name }} {{ s.last_name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.amount') }}</label>
          <input v-model.number="contributionForm.amount" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('expenses.description') }}</label>
          <input v-model="contributionForm.description" type="text" class="input" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeContributionModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <ConfirmDialog
      v-model="deleteShareholderDialogOpen"
      :message="deleteShareholderDialogMessage"
      :loading="deleteShareholderLoading"
      @confirm="doConfirmDeleteShareholder"
    />
    <ConfirmDialog
      v-model="deleteContributionDialogOpen"
      :message="deleteContributionDialogMessage"
      :loading="deleteContributionLoading"
      @confirm="doConfirmDeleteContribution"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { getShareholders, createShareholder, updateShareholder, deleteShareholder, getContributions, createContribution, updateContribution, deleteContribution } from '../api/contributions'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const shareholders = ref([])
const contributions = ref([])
const loading = ref(false)
const shareholderModalOpen = ref(false)
const contributionModalOpen = ref(false)
const editingShareholder = ref(null)
const editingContribution = ref(null)
const deleteShareholderDialogOpen = ref(false)
const itemToDeleteShareholder = ref(null)
const deleteShareholderLoading = ref(false)
const deleteContributionDialogOpen = ref(false)
const itemToDeleteContribution = ref(null)
const deleteContributionLoading = ref(false)

const shareholderModalTitle = computed(() =>
  editingShareholder.value ? `${t('common.edit')} ${t('shareholders.title')}` : `${t('common.add')} ${t('shareholders.title')}`
)
const contributionModalTitle = computed(() =>
  editingContribution.value ? `${t('common.edit')} ${t('financing.contribution')}` : `${t('common.add')} ${t('financing.contribution')}`
)

const contributionsTotal = computed(() =>
  contributions.value.reduce((sum, c) => sum + (Number(c.amount) || 0), 0)
)

const deleteShareholderDialogMessage = computed(() => {
  if (!itemToDeleteShareholder.value) return ''
  const name = `${itemToDeleteShareholder.value.first_name} ${itemToDeleteShareholder.value.last_name}`
  return `${name} — ${t('financing.confirmDeleteShareholder')}`
})
const deleteContributionDialogMessage = computed(() =>
  itemToDeleteContribution.value ? `${itemToDeleteContribution.value.date} — ${t('financing.confirmDeleteContribution')}` : ''
)

const shareholderColumns = computed(() => [
  { key: 'first_name', label: t('shareholders.firstName') },
  { key: 'last_name', label: t('shareholders.lastName') },
  { key: 'email', label: t('shareholders.email') },
  {
    key: 'total_contributions',
    label: t('financing.totalContributions'),
    value: (item) => {
      const total = contributions.value
        .filter((c) => c.shareholder_id === item.id)
        .reduce((sum, c) => sum + (Number(c.amount) || 0), 0)
      return formatAmount(total)
    },
  },
])

const contributionColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'amount', label: t('financing.amount'), value: (item) => formatAmount(item.amount) },
  { key: 'description', label: t('expenses.description') },
  {
    key: 'shareholder_id',
    label: t('financing.shareholder'),
    value: (item) => {
      const s = shareholders.value.find((sh) => sh.id === item.shareholder_id)
      return s ? `${s.first_name || ''} ${s.last_name || ''}`.trim() || '—' : '—'
    },
  },
])
const shareholderForm = ref({ first_name: '', last_name: '', phone: '', email: '' })
const contributionForm = ref({
  date: new Date().toISOString().slice(0, 10),
  shareholder_id: '',
  amount: 0,
  description: '',
})

function openAddShareholder() {
  editingShareholder.value = null
  shareholderForm.value = { first_name: '', last_name: '', phone: '', email: '' }
  shareholderModalOpen.value = true
}

function closeShareholderModal() {
  shareholderModalOpen.value = false
  editingShareholder.value = null
}

function startEditShareholder(item) {
  editingShareholder.value = item.id
  shareholderForm.value = {
    first_name: item.first_name,
    last_name: item.last_name,
    phone: item.phone || '',
    email: item.email || '',
  }
  shareholderModalOpen.value = true
}

function confirmDeleteShareholder(item) {
  itemToDeleteShareholder.value = item
  deleteShareholderDialogOpen.value = true
}

async function doConfirmDeleteShareholder() {
  if (!itemToDeleteShareholder.value) return
  deleteShareholderLoading.value = true
  try {
    await deleteShareholder(itemToDeleteShareholder.value.id)
    deleteShareholderDialogOpen.value = false
    itemToDeleteShareholder.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteShareholderLoading.value = false
  }
}

function openAddContribution() {
  editingContribution.value = null
  contributionForm.value = { date: new Date().toISOString().slice(0, 10), shareholder_id: '', amount: 0, description: '' }
  contributionModalOpen.value = true
}

function closeContributionModal() {
  contributionModalOpen.value = false
  editingContribution.value = null
}

function startEditContribution(item) {
  editingContribution.value = item.id
  contributionForm.value = {
    date: item.date,
    shareholder_id: item.shareholder_id || '',
    amount: item.amount ?? 0,
    description: item.description || '',
  }
  contributionModalOpen.value = true
}

function confirmDeleteContribution(item) {
  itemToDeleteContribution.value = item
  deleteContributionDialogOpen.value = true
}

async function doConfirmDeleteContribution() {
  if (!itemToDeleteContribution.value) return
  deleteContributionLoading.value = true
  try {
    await deleteContribution(itemToDeleteContribution.value.id)
    deleteContributionDialogOpen.value = false
    itemToDeleteContribution.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteContributionLoading.value = false
  }
}

async function load() {
  loading.value = true
  try {
    shareholders.value = await getShareholders()
    contributions.value = await getContributions()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitShareholder() {
  try {
    if (editingShareholder.value) {
      await updateShareholder(editingShareholder.value, shareholderForm.value)
    } else {
      await createShareholder(shareholderForm.value)
    }
    closeShareholderModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submitContribution() {
  try {
    if (editingContribution.value) {
      await updateContribution(editingContribution.value, contributionForm.value)
    } else {
      await createContribution(contributionForm.value)
    }
    closeContributionModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

<style scoped>
.financing-total {
  margin: 0 0 var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
.financing-total strong {
  color: var(--color-text);
}
</style>
