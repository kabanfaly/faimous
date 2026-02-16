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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import PaginatedTable from '../components/PaginatedTable.vue'
import Modal from '../components/Modal.vue'
import IconButton from '../components/IconButton.vue'
import PageHeader from '../components/PageHeader.vue'
import { getExpenses, getCategories, createExpense, updateExpense, deleteExpense } from '../api/expenses'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const expenses = ref([])
const categories = ref([])
const loading = ref(false)
const expenseModalOpen = ref(false)
const editingExpense = ref(null)

const expenseModalTitle = computed(() =>
  editingExpense.value ? `${t('common.edit')} ${t('expenses.title')}` : `${t('common.add')} ${t('expenses.title')}`
)

const expenseColumns = computed(() => [
  { key: 'date', label: t('common.date') },
  { key: 'description', label: t('expenses.description') },
  { key: 'amount', label: t('expenses.amount'), value: (item) => formatAmount(item.amount) },
  { key: 'category_id', label: t('expenses.category') },
])
const expenseForm = ref({
  date: new Date().toISOString().slice(0, 10),
  description: '',
  category_id: '',
  amount: 0,
})

function openAddExpense() {
  editingExpense.value = null
  expenseForm.value = { date: new Date().toISOString().slice(0, 10), description: '', category_id: '', amount: 0 }
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
    category_id: item.category_id || '',
    amount: item.amount ?? 0,
  }
  expenseModalOpen.value = true
}

function confirmDelete(item) {
  const desc = item.description || item.id
  if (window.confirm(`${desc} — ${t('expenses.confirmDelete')}`)) doDeleteExpense(item.id)
}

async function doDeleteExpense(id) {
  try {
    await deleteExpense(id)
    await load()
  } catch (e) {
    console.error(e)
  }
}

async function load() {
  loading.value = true
  try {
    const [expensesData, categoriesData] = await Promise.all([getExpenses(), getCategories()])
    expenses.value = expensesData
    categories.value = categoriesData
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function submitExpense() {
  try {
    if (editingExpense.value) {
      await updateExpense(editingExpense.value, expenseForm.value)
    } else {
      await createExpense(expenseForm.value)
    }
    closeExpenseModal()
    await load()
  } catch (e) {
    console.error(e)
  }
}

onMounted(load)
</script>

