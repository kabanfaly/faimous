<template>
  <div class="page">
    <PageHeader>
      {{ $t('stock.title') }}
      <template #subtitle>{{ $t('stock.products') }} · {{ $t('stock.movements') }} · {{ $t('stock.alerts') }}</template>
    </PageHeader>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('stock.products') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddProduct">{{ $t('common.add') }} {{ $t('stock.products') }}</button>
      </div>
      <PaginatedTable
        :items="products"
        :columns="productColumns"
        :loading="loading"
        :empty-text="$t('stock.emptyProducts')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditProduct(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteProduct(item)" />
        </template>
      </PaginatedTable>
    </section>
    <section class="card card-body" style="margin-bottom: var(--space-6);">
      <div class="section-header">
        <h2 class="section-title">{{ $t('stock.movements') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddMovement">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="movements"
        :columns="movementColumns"
        :loading="loading"
        :empty-text="$t('stock.emptyMovements')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEditMovement(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDeleteMovement(item)" />
        </template>
      </PaginatedTable>
    </section>
    <section v-if="alerts.length" class="card card-body">
      <h2 class="section-title">{{ $t('stock.alerts') }}</h2>
      <PaginatedTable
        :items="alerts"
        :columns="alertColumns"
        :loading="false"
        :empty-text="$t('stock.emptyAlerts')"
        :per-page="10"
      />
    </section>

    <Modal v-model="productModalOpen" :title="productModalTitle">
      <form @submit.prevent="submitProduct" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('products.name') }}</label>
          <input v-model="productForm.name" type="text" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('products.unit') }}</label>
          <input v-model="productForm.unit" type="text" class="input" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeProductModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="movementModalOpen" :title="movementModalTitle">
      <form @submit.prevent="submitMovement" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="movementForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('stock.product') }}</label>
          <select v-model="movementForm.product_id" class="input" required>
            <option value="">{{ $t('common.selectProduct') }}</option>
            <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.quantity') }}</label>
          <input v-model.number="movementForm.quantity" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-group">
          <label>{{ $t('stock.type') }}</label>
          <input v-model="movementForm.movement_type" type="text" class="input" :placeholder="$t('stock.typePlaceholder')" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeMovementModal">{{ $t('common.cancel') }}</button>
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
import { getProducts, createProduct, updateProduct, deleteProduct, getMovements, createMovement, updateMovement, deleteMovement, getAlerts } from '../api/stock'

const { t } = useI18n()
const products = ref([])
const movements = ref([])
const alerts = ref([])
const loading = ref(false)
const productModalOpen = ref(false)
const movementModalOpen = ref(false)
const editingProduct = ref(null)
const editingMovement = ref(null)

const productModalTitle = computed(() =>
  editingProduct.value ? `${t('common.edit')} ${t('stock.products')}` : `${t('common.add')} ${t('stock.products')}`
)
const movementModalTitle = computed(() =>
  editingMovement.value ? `${t('common.edit')} ${t('stock.movements')}` : `${t('common.add')} ${t('stock.movements')}`
)

const productColumns = computed(() => [
  { key: 'name', label: t('products.name') },
  { key: 'unit', label: t('products.unit') },
  { key: 'description', label: t('products.description') },
])

const movementColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'product_id', label: t('stock.product') },
  { key: 'quantity', label: t('stock.quantity') },
  { key: 'movement_type', label: t('stock.type') },
])

const alertColumns = computed(() => [
  { key: 'product_name', label: t('products.name') },
  { key: 'balance', label: t('stock.balance') },
])
const productForm = ref({ name: '', unit: '' })
const movementForm = ref({
  date: new Date().toISOString().slice(0, 10),
  product_id: '',
  quantity: 0,
  movement_type: 'in',
})

function openAddProduct() {
  editingProduct.value = null
  productForm.value = { name: '', unit: '' }
  productModalOpen.value = true
}

function closeProductModal() {
  productModalOpen.value = false
  editingProduct.value = null
}

function startEditProduct(item) {
  editingProduct.value = item.id
  productForm.value = { name: item.name, unit: item.unit || '' }
  productModalOpen.value = true
}

function confirmDeleteProduct(item) {
  if (window.confirm(`${item.name} — ${t('stock.confirmDeleteProduct')}`)) doDeleteProduct(item.id)
}

async function doDeleteProduct(id) {
  try {
    await deleteProduct(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

function openAddMovement() {
  editingMovement.value = null
  movementForm.value = { date: new Date().toISOString().slice(0, 10), product_id: '', quantity: 0, movement_type: 'in' }
  movementModalOpen.value = true
}

function closeMovementModal() {
  movementModalOpen.value = false
  editingMovement.value = null
}

function startEditMovement(item) {
  editingMovement.value = item.id
  movementForm.value = {
    date: item.date,
    product_id: item.product_id || '',
    quantity: item.quantity ?? 0,
    movement_type: item.movement_type || 'in',
  }
  movementModalOpen.value = true
}

function confirmDeleteMovement(item) {
  if (window.confirm(`${item.date} — ${t('stock.confirmDeleteMovement')}`)) doDeleteMovement(item.id)
}

async function doDeleteMovement(id) {
  try {
    await deleteMovement(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function load() {
  loading.value = true
  try {
    products.value = await getProducts()
    movements.value = await getMovements()
    alerts.value = await getAlerts()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitProduct() {
  try {
    if (editingProduct.value) {
      await updateProduct(editingProduct.value, productForm.value)
    } else {
      await createProduct(productForm.value)
    }
    closeProductModal()
    productForm.value = { name: '', unit: '' }
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function submitMovement() {
  try {
    if (editingMovement.value) {
      await updateMovement(editingMovement.value, movementForm.value)
    } else {
      await createMovement(movementForm.value)
    }
    closeMovementModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

