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
          <label>{{ $t('purchases.supplier') }}</label>
          <select v-model="form.supplier_id" class="input">
            <option value="">{{ $t('common.selectSupplier') }}</option>
            <option v-for="s in suppliers" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('stock.product') }}</label>
          <select v-model="form.product_id" class="input">
            <option value="">{{ $t('common.selectProduct') }}</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
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
          <label class="required">{{ $t('purchases.purchase') }}</label>
          <select v-model="paymentForm.purchase_id" class="input" required>
            <option value="">{{ $t('common.selectPurchase') }}</option>
            <option v-for="p in unpaid" :key="p.id" :value="p.id">{{ p.date }} — {{ formatAmount(p.total_price) }}</option>
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
import { createPurchase, addPayment, getUnpaid, getPurchase, updatePurchase, deletePurchase } from '../api/purchases'
import { getSuppliers } from '../api/suppliers'
import { getProducts } from '../api/products'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const unpaid = ref([])
const suppliers = ref([])
const products = ref([])
const loading = ref(false)
const purchaseModalOpen = ref(false)
const paymentModalOpen = ref(false)
const editingPurchase = ref(null)
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const purchaseModalTitle = computed(() =>
  editingPurchase.value ? `${t('common.edit')} ${t('purchases.title')}` : `${t('common.add')} ${t('purchases.title')}`
)

const deleteDialogMessage = computed(() =>
  itemToDelete.value ? `${itemToDelete.value.date} — ${t('purchases.confirmDelete')}` : ''
)

const columns = computed(() => [
  { key: 'date', label: t('common.date') },
  {
    key: 'supplier_id',
    label: t('purchases.supplier'),
    value: (item) => {
      const s = suppliers.value.find((x) => x.id === item.supplier_id)
      return s?.name ?? '—'
    },
  },
  {
    key: 'product_id',
    label: t('stock.product'),
    value: (item) => {
      const p = products.value.find((x) => x.id === item.product_id)
      return p?.name ?? '—'
    },
  },
  { key: 'total_price', label: t('purchases.total'), value: (item) => formatAmount(item.total_price) },
  { key: 'status', label: t('purchases.status') },
])
const form = ref({
  date: new Date().toISOString().slice(0, 10),
  supplier_id: '',
  product_id: '',
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
  form.value = {
    date: new Date().toISOString().slice(0, 10),
    supplier_id: '',
    product_id: '',
    quantity: 0,
    unit_price: 0,
    total_price: 0,
    status: 'unpaid',
  }
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
      product_id: p.product_id || '',
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
  itemToDelete.value = item
  deleteDialogOpen.value = true
}

async function doConfirmDelete() {
  if (!itemToDelete.value) return
  deleteLoading.value = true
  try {
    await deletePurchase(itemToDelete.value.id)
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
    const [unpaidData, suppliersData, productsData] = await Promise.all([
      getUnpaid(),
      getSuppliers(),
      getProducts(),
    ])
    unpaid.value = unpaidData
    suppliers.value = suppliersData
    products.value = productsData
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

