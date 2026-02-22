<template>
  <div class="page">
    <PageHeader>{{ $t('expenses.title') }}</PageHeader>
    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('expenses.title') }}</h2>
        <button type="button" class="btn btn-primary" @click="openAddExpense">{{ $t('common.add') }}</button>
      </div>
      <PaginatedTable
        :items="expenses"
        :columns="expenseColumns"
        :loading="loading"
        :empty-text="$t('expenses.empty')"
        :per-page="10"
      >
        <template #actions="{ item }">
          <IconButton type="edit" :title="$t('common.edit')" @click="startEdit(item)" />
          <IconButton type="delete" :title="$t('common.delete')" @click="confirmDelete(item)" />
        </template>
      </PaginatedTable>
    </section>

    <Modal v-model="expenseModalOpen" :title="expenseModalTitle">
      <form @submit.prevent="submitExpense" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="expenseForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('expenses.description') }}</label>
          <input v-model="expenseForm.description" type="text" class="input" />
        </div>
        <div class="form-group">
          <label>{{ $t('expenses.farm') }}</label>
          <select v-model="expenseForm.farm_id" class="input">
            <option value="">{{ $t('common.selectFarm') }}</option>
            <option v-for="f in farms" :key="f.id" :value="f.id">{{ f.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>{{ $t('expenses.category') }}</label>
          <select v-model="expenseForm.category_id" class="input">
            <option value="">{{ $t('common.selectCategory') }}</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label class="required">{{ $t('common.amount') }}</label>
          <input v-model.number="expenseForm.amount" type="number" class="input" step="0.01" required />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="closeExpenseModal">{{ $t('common.cancel') }}</button>
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
import { getExpenses, getCategories, createExpense, updateExpense, deleteExpense } from '../api/expenses'
import { getFarms } from '../api/farms'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const expenses = ref([])
const categories = ref([])
const farms = ref([])
const loading = ref(false)
const expenseModalOpen = ref(false)
const editingExpense = ref(null)
const deleteDialogOpen = ref(false)
const itemToDelete = ref(null)
const deleteLoading = ref(false)

const expenseModalTitle = computed(() =>
  editingExpense.value ? `${t('common.edit')} ${t('expenses.title')}` : `${t('common.add')} ${t('expenses.title')}`
)

const deleteDialogMessage = computed(() => {
  if (!itemToDelete.value) return ''
  const desc = itemToDelete.value.description || itemToDelete.value.id
  return `${desc} — ${t('expenses.confirmDelete')}`
})

const expenseColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'description', label: t('expenses.description') },
  { key: 'amount', label: t('expenses.amount'), value: (item) => formatAmount(item.amount) },
  {
    key: 'category_id',
    label: t('expenses.category'),
    value: (item) => {
      const cat = categories.value.find((c) => c.id === item.category_id)
      return cat?.name ?? '—'
    },
  },
  {
    key: 'farm_id',
    label: t('expenses.farm'),
    value: (item) => {
      const farm = farms.value.find((f) => f.id === item.farm_id)
      return farm?.name ?? '—'
    },
  },
])
const expenseForm = ref({
  date: new Date().toISOString().slice(0, 10),
  description: '',
  farm_id: '',
  category_id: '',
  amount: 0,
})

function openAddExpense() {
  editingExpense.value = null
  expenseForm.value = { date: new Date().toISOString().slice(0, 10), description: '', farm_id: '', category_id: '', amount: 0 }
  expenseModalOpen.value = true
}

function closeExpenseModal() {
  expenseModalOpen.value = false
  editingExpense.value = null
}

function startEdit(item) {
  editingExpense.value = item.id
  expenseForm.value = {
    date: item.date,
    description: item.description || '',
    farm_id: item.farm_id || '',
    category_id: item.category_id || '',
    amount: item.amount ?? 0,
  }
  expenseModalOpen.value = true
}

function confirmDelete(item) {
  itemToDelete.value = item
  deleteDialogOpen.value = true
}

async function doConfirmDelete() {
  if (!itemToDelete.value) return
  deleteLoading.value = true
  try {
    await deleteExpense(itemToDelete.value.id)
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
    const [expensesData, categoriesData, farmsData] = await Promise.all([
      getExpenses(),
      getCategories(),
      getFarms(),
    ])
    expenses.value = expensesData
    categories.value = categoriesData
    farms.value = farmsData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitExpense() {
  try {
    if (editingExpense.value) {
      await updateExpense(editingExpense.value, {
      ...expenseForm.value,
      farm_id: expenseForm.value.farm_id || undefined,
    })
    } else {
      await createExpense({
      ...expenseForm.value,
      farm_id: expenseForm.value.farm_id || undefined,
    })
    }
    closeExpenseModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

