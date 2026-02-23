<template>
  <div class="page">
    <PageHeader>
      {{ $t('stock.title') }}
      <template #subtitle>{{ $t('stock.products') }} · {{ $t('stock.alerts') }}</template>
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
          <label>{{ $t('common.quantity') }}</label>
          <input v-model.number="productForm.quantity" type="number" class="input" step="0.01" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('products.unit') }}</label>
          <select v-model="productForm.unit" class="input">
            <option value="">{{ $t('common.selectUnit') }}</option>
            <option v-for="u in productUnits" :key="u" :value="u">{{ u }}</option>
          </select>
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeProductModal">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <ConfirmDialog
      v-model="deleteProductDialogOpen"
      :message="deleteProductDialogMessage"
      :loading="deleteProductLoading"
      @confirm="doConfirmDeleteProduct"
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
import { getProducts, createProduct, updateProduct, deleteProduct, getProductUnits } from '../api/products'
import { getAlerts } from '../api/stock'
import { getProductTypes } from '../api/productTypes'

const { t } = useI18n()
const products = ref([])
const productTypes = ref([])
const productUnits = ref([])
const alerts = ref([])
const loading = ref(false)
const productModalOpen = ref(false)
const editingProduct = ref(null)
const deleteProductDialogOpen = ref(false)
const itemToDeleteProduct = ref(null)
const deleteProductLoading = ref(false)

const productModalTitle = computed(() =>
  editingProduct.value ? `${t('common.edit')} ${t('stock.products')}` : `${t('common.add')} ${t('stock.products')}`
)

const deleteProductDialogMessage = computed(() =>
  itemToDeleteProduct.value ? `${itemToDeleteProduct.value.name} — ${t('stock.confirmDeleteProduct')}` : ''
)

const productColumns = computed(() => [
  { key: 'name', label: t('products.name') },
  { key: 'quantity', label: t('common.quantity') },
  {
    key: 'product_type',
    label: t('products.type'),
    value: (item) => item.product_type?.name ?? '—',
  },
  { key: 'unit', label: t('products.unit') },
  { key: 'description', label: t('products.description') },
])

const alertColumns = computed(() => [
  { key: 'product_name', label: t('products.name') },
  { key: 'balance', label: t('stock.balance') },
])
const productForm = ref({ name: '', description: '', product_type_id: '', quantity: null, unit: '' })

function openAddProduct() {
  editingProduct.value = null
  productForm.value = { name: '', description: '', product_type_id: '', quantity: null, unit: '' }
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
    quantity: item.quantity ?? null,
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

async function load() {
  loading.value = true
  try {
    const [productsData, typesData, unitsData, alertsData] = await Promise.all([
      getProducts(),
      getProductTypes(),
      getProductUnits(),
      getAlerts(),
    ])
    products.value = productsData
    productTypes.value = typesData
    productUnits.value = unitsData
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
      quantity: productForm.value.quantity ?? undefined,
      unit: productForm.value.unit || undefined,
    }
    if (editingProduct.value) {
      await updateProduct(editingProduct.value, payload)
    } else {
      await createProduct(payload)
    }
    closeProductModal()
    productForm.value = { name: '', description: '', product_type_id: '', quantity: null, unit: '' }
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

