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
          <label>{{ $t('products.description') }}</label>
          <input v-model="productForm.description" type="text" class="input" />
        </div>
        <div class="form-group">
          <label class="required">{{ $t('products.type') }}</label>
          <select v-model="productForm.product_type_id" class="input" required>
            <option value="" disabled>{{ $t('common.selectProduct') }}</option>
            <option v-for="pt in productTypes" :key="pt.id" :value="pt.id">{{ pt.name }}</option>
          </select>
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

    <ConfirmDialog
      v-model="deleteProductDialogOpen"
      :message="deleteProductDialogMessage"
      :loading="deleteProductLoading"
      @confirm="doConfirmDeleteProduct"
    />
    <ConfirmDialog
      v-model="deleteMovementDialogOpen"
      :message="deleteMovementDialogMessage"
      :loading="deleteMovementLoading"
      @confirm="doConfirmDeleteMovement"
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
import { getProducts, createProduct, updateProduct, deleteProduct, getMovements, createMovement, updateMovement, deleteMovement, getAlerts } from '../api/stock'
import { getProductTypes } from '../api/productTypes'

const { t } = useI18n()
const products = ref([])
const productTypes = ref([])
const movements = ref([])
const alerts = ref([])
const loading = ref(false)
const productModalOpen = ref(false)
const movementModalOpen = ref(false)
const editingProduct = ref(null)
const editingMovement = ref(null)
const deleteProductDialogOpen = ref(false)
const itemToDeleteProduct = ref(null)
const deleteProductLoading = ref(false)
const deleteMovementDialogOpen = ref(false)
const itemToDeleteMovement = ref(null)
const deleteMovementLoading = ref(false)

const productModalTitle = computed(() =>
  editingProduct.value ? `${t('common.edit')} ${t('stock.products')}` : `${t('common.add')} ${t('stock.products')}`
)
const movementModalTitle = computed(() =>
  editingMovement.value ? `${t('common.edit')} ${t('stock.movements')}` : `${t('common.add')} ${t('stock.movements')}`
)

const deleteProductDialogMessage = computed(() =>
  itemToDeleteProduct.value ? `${itemToDeleteProduct.value.name} — ${t('stock.confirmDeleteProduct')}` : ''
)
const deleteMovementDialogMessage = computed(() =>
  itemToDeleteMovement.value ? `${itemToDeleteMovement.value.date} — ${t('stock.confirmDeleteMovement')}` : ''
)

const productColumns = computed(() => [
  { key: 'name', label: t('products.name') },
  {
    key: 'product_type',
    label: t('products.type'),
    value: (item) => item.product_type?.name ?? '—',
  },
  { key: 'unit', label: t('products.unit') },
  { key: 'description', label: t('products.description') },
])

const movementColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  {
    key: 'product_id',
    label: t('stock.product'),
    value: (item) => {
      const p = products.value.find((x) => x.id === item.product_id)
      return p?.name ?? item.product_id ?? '—'
    },
  },
  { key: 'quantity', label: t('stock.quantity') },
  { key: 'movement_type', label: t('stock.type') },
])

const alertColumns = computed(() => [
  { key: 'product_name', label: t('products.name') },
  { key: 'balance', label: t('stock.balance') },
])
const productForm = ref({ name: '', description: '', product_type_id: '', unit: '' })
const movementForm = ref({
  date: new Date().toISOString().slice(0, 10),
  product_id: '',
  quantity: 0,
  movement_type: 'in',
})

function openAddProduct() {
  editingProduct.value = null
  productForm.value = { name: '', description: '', product_type_id: '', unit: '' }
  productModalOpen.value = true
}

function closeProductModal() {
  productModalOpen.value = false
  editingProduct.value = null
}

function startEditProduct(item) {
  editingProduct.value = item.id
  productForm.value = {
    name: item.name,
    description: item.description || '',
    product_type_id: item.product_type_id || '',
    unit: item.unit || '',
  }
  productModalOpen.value = true
}

function confirmDeleteProduct(item) {
  itemToDeleteProduct.value = item
  deleteProductDialogOpen.value = true
}

async function doConfirmDeleteProduct() {
  if (!itemToDeleteProduct.value) return
  deleteProductLoading.value = true
  try {
    await deleteProduct(itemToDeleteProduct.value.id)
    deleteProductDialogOpen.value = false
    itemToDeleteProduct.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteProductLoading.value = false
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
  itemToDeleteMovement.value = item
  deleteMovementDialogOpen.value = true
}

async function doConfirmDeleteMovement() {
  if (!itemToDeleteMovement.value) return
  deleteMovementLoading.value = true
  try {
    await deleteMovement(itemToDeleteMovement.value.id)
    deleteMovementDialogOpen.value = false
    itemToDeleteMovement.value = null
    await load()
  } catch (e) {
    console.error(e)
  } finally {
    deleteMovementLoading.value = false
  }
}

async function load() {
  loading.value = true
  try {
    const [productsData, typesData, movementsData, alertsData] = await Promise.all([
      getProducts(),
      getProductTypes(),
      getMovements(),
      getAlerts(),
    ])
    products.value = productsData
    productTypes.value = typesData
    movements.value = movementsData
    alerts.value = alertsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitProduct() {
  try {
    const payload = {
      ...productForm.value,
      product_type_id: productForm.value.product_type_id || undefined,
    }
    if (editingProduct.value) {
      await updateProduct(editingProduct.value, payload)
    } else {
      await createProduct(payload)
    }
    closeProductModal()
    productForm.value = { name: '', description: '', product_type_id: '', unit: '' }
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

