<template>
  <div class="page">
    <PageHeader>
      {{ $t('sales.title') }}
      <template #subtitle>{{ $t('sales.unpaid') }} · {{ $t('sales.payments') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('sales.unpaid') }}</h2>
        <div class="section-actions">
          <button type="button" class="btn btn-primary" @click="openAddSale">{{ $t('common.add') }} {{ $t('sales.title') }}</button>
          <button type="button" class="btn btn-ghost" @click="paymentModalOpen = true">{{ $t('sales.payments') }}</button>
        </div>
      </div>
      <PaginatedTable
        :items="unpaid"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('sales.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="saleModalOpen" :title="saleModalTitle">
      <form @submit.prevent="submitSale" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="form.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('dailyOperations.farm') }}</label>
          <select v-model="form.farm_id" class="input">
            <option value="">{{ $t('common.selectFarm') }}</option>
            <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('common.quantity') }}</label>
          <input v-model.number="form.quantity" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('common.unitPrice') }}</label>
          <input v-model.number="form.unit_price" type="number" class="input" step="0.01" />
        </div>
        <div class="form-group">
          <label>{{ $t('common.total') }}</label>
          <input v-model.number="form.total_price" type="number" class="input" step="0.01" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeSaleModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="paymentModalOpen" :title="$t('sales.payments')">
      <form @submit.prevent="submitPayment" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('sales.sale') }}</label>
          <select v-model="paymentForm.sale_id" class="input" required>
            <option value="">{{ $t('common.selectSale') }}</option>
            <option v-for="s in unpaid" :key="s.id" :value="s.id">{{ s.date }} — {{ formatAmount(s.total_price) }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="paymentForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.amount') }}</label>
          <input v-model.number="paymentForm.amount" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="paymentModalOpen = false">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <ConfirmDialog
      v-model="deleteDialogOpen"
      :message="deleteDialogMessage"
      :loading="deleteLoading"
      @confirm="doConfirmDelete"
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
import { createSale, addPayment, getUnpaid, getSale, updateSale, deleteSale } from '../api/sales'
import { getFarms } from '../api/farms'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const unpaid = ref([])
const farms = ref([])
const loading = ref(false)
const saleModalOpen = ref(false)
const paymentModalOpen = ref(false)
const editingSale = ref(null)
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const saleModalTitle = computed(() =>
  editingSale.value ? `${t('common.edit')} ${t('sales.title')}` : `${t('common.add')} ${t('sales.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.date} — ${t('sales.confirmDelete')}` : ''
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  {
    key: 'farm_id',
    label: t('dailyOperations.farm'),
    value: (item) => {
      const farm = farms.value.find((f) => f.id === item.farm_id)
      return farm?.name ?? '—'
    },
  },
  { key: 'total_price', label: t('sales.total'), value: (item) => formatAmount(item.total_price) },
  { key: 'payment_status', label: t('sales.status') },
])
const form = ref({
  date: new Date().toISOString().slice(0, 10),
  farm_id: '',
  quantity: 0,
  unit_price: 0,
  total_price: 0,
  payment_status: 'unpaid',
})
const paymentForm = ref({
  sale_id: '',
  date: new Date().toISOString().slice(0, 10),
  amount: 0,
})

function openAddSale() {
  editingSale.value = null
  form.value = {
    date: new Date().toISOString().slice(0, 10),
    farm_id: '',
    quantity: 0,
    unit_price: 0,
    total_price: 0,
    payment_status: 'unpaid',
  }
  saleModalOpen.value = true
}

function closeSaleModal() {
  saleModalOpen.value = false
  editingSale.value = null
}

async function startEdit(item) {
  try {
    const s = await getSale(item.id)
    editingSale.value = item.id
    form.value = {
      date: s.date,
      farm_id: s.farm_id || '',
      quantity: s.quantity ?? 0,
      unit_price: s.unit_price ?? 0,
      total_price: s.total_price ?? 0,
      payment_status: s.payment_status || 'unpaid',
    }
    saleModalOpen.value = true
  } catch (e) {
    console.error(e)
  }
}

function confirmDelete(item) {
  itemToDelete.value = item
  deleteDialogOpen.value = true
}

async function doConfirmDelete() {
  if (!itemToDelete.value) return
  deleteLoading.value = true
  try {
    await deleteSale(itemToDelete.value.id)
    deleteDialogOpen.value = false
    itemToDelete.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteLoading.value = false
  }
}

async function load() {
  loading.value = true
  try {
    const [unpaidData, farmsData] = await Promise.all([getUnpaid(), getFarms()])
    unpaid.value = unpaidData
    farms.value = farmsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitSale() {
  try {
    const payload = { ...form.value, farm_id: form.value.farm_id || undefined }
    if (editingSale.value) {
      await updateSale(editingSale.value, payload)
    } else {
      await createSale(payload)
    }
    closeSaleModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submitPayment() {
  try {
    await addPayment(paymentForm.value)
    paymentModalOpen.value = false
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

