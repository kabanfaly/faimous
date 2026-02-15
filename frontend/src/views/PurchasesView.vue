<template>
  <div class="page">
    <PageHeader>
      {{ $t('purchases.title') }}
      <template #subtitle>{{ $t('purchases.unpaid') }} · {{ $t('purchases.supplierPayments') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('purchases.unpaid') }}</h2>
        <div class="section-actions">
          <button type="button" class="btn btn-primary" @click="openAddPurchase">{{ $t('common.add') }} {{ $t('purchases.title') }}</button>
          <button type="button" class="btn btn-ghost" @click="paymentModalOpen = true">{{ $t('purchases.supplierPayments') }}</button>
        </div>
      </div>
      <PaginatedTable
        :items="unpaid"
        :columns="columns"
        :loading="loading"
        :empty-text="$t('purchases.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="purchaseModalOpen" :title="purchaseModalTitle">
      <form @submit.prevent="submitPurchase" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="form.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('purchases.supplierId') }}</label>
          <select v-model="form.supplier_id" class="input">
            <option value=""></option>
            <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('common.quantity') }}</label>
          <input v-model.number="form.quantity" type="number" class="input" step="0.01" />
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
          <button type="button" class="btn btn-ghost" @click="closePurchaseModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="paymentModalOpen" :title="$t('purchases.supplierPayments')">
      <form @submit.prevent="submitPayment" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('purchases.purchaseId') }}</label>
          <select v-model="paymentForm.purchase_id" class="input" required>
            <option value="">—</option>
            <option v-for="p in unpaid" :key="p.id" :value="p.id">{{ p.date }} — {{ p.total_price }}</option>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { createPurchase, addPayment, getUnpaid, getPurchase, updatePurchase, deletePurchase } from '../api/purchases'
import { getSuppliers } from '../api/suppliers'

const { t } = useI18n()
const unpaid = ref([])
const suppliers = ref([])
const loading = ref(false)
const purchaseModalOpen = ref(false)
const paymentModalOpen = ref(false)
const editingPurchase = ref(null)

const purchaseModalTitle = computed(() =>
  editingPurchase.value ? `${t('common.edit')} ${t('purchases.title')}` : `${t('common.add')} ${t('purchases.title')}`
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'total_price', label: t('purchases.total') },
  { key: 'status', label: t('purchases.status') },
])
const form = ref({
  date: new Date().toISOString().slice(0, 10),
  supplier_id: '',
  quantity: 0,
  unit_price: 0,
  total_price: 0,
  status: 'unpaid',
})
const paymentForm = ref({
  purchase_id: '',
  date: new Date().toISOString().slice(0, 10),
  amount: 0,
})

function openAddPurchase() {
  editingPurchase.value = null
  form.value = { date: new Date().toISOString().slice(0, 10), supplier_id: '', quantity: 0, unit_price: 0, total_price: 0, status: 'unpaid' }
  purchaseModalOpen.value = true
}

function closePurchaseModal() {
  purchaseModalOpen.value = false
  editingPurchase.value = null
}

async function startEdit(item) {
  try {
    const p = await getPurchase(item.id)
    editingPurchase.value = item.id
    form.value = {
      date: p.date,
      supplier_id: p.supplier_id || '',
      quantity: p.quantity ?? 0,
      unit_price: p.unit_price ?? 0,
      total_price: p.total_price ?? 0,
      status: p.status || 'unpaid',
    }
    purchaseModalOpen.value = true
  } catch (e) {
    console.error(e)
  }
}

function confirmDelete(item) {
  if (window.confirm(`${item.date} — ${t('purchases.confirmDelete')}`)) doDeletePurchase(item.id)
}

async function doDeletePurchase(id) {
  try {
    await deletePurchase(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function load() {
  loading.value = true
  try {
    const [unpaidData, suppliersData] = await Promise.all([getUnpaid(), getSuppliers()])
    unpaid.value = unpaidData
    suppliers.value = suppliersData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitPurchase() {
  try {
    if (editingPurchase.value) {
      await updatePurchase(editingPurchase.value, form.value)
    } else {
      await createPurchase(form.value)
    }
    closePurchaseModal()
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

