<template>
  <div class="page">
    <PageHeader>
      {{ $t('stock.movements') }}
      <template #subtitle>{{ $t('stock.title') }}</template>
    </PageHeader>
    <section class="card card-body">
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
import { getProducts } from '../api/products'
import { getMovements, createMovement, updateMovement, deleteMovement } from '../api/stock'

const { t } = useI18n()
const products = ref([])
const movements = ref([])
const loading = ref(false)
const movementModalOpen = ref(false)
const editingMovement = ref(null)
const deleteMovementDialogOpen = ref(false)
const itemToDeleteMovement = ref(null)
const deleteMovementLoading = ref(false)

const movementModalTitle = computed(() =>
  editingMovement.value ? `${t('common.edit')} ${t('stock.movements')}` : `${t('common.add')} ${t('stock.movements')}`
)

const deleteMovementDialogMessage = computed(() =>
  itemToDeleteMovement.value ? `${itemToDeleteMovement.value.date} — ${t('stock.confirmDeleteMovement')}` : ''
)

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

const movementForm = ref({
  date: new Date().toISOString().slice(0, 10),
  product_id: '',
  quantity: 0,
  movement_type: 'in',
})

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
    const [productsData, movementsData] = await Promise.all([getProducts(), getMovements()])
    products.value = productsData
    movements.value = movementsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
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
