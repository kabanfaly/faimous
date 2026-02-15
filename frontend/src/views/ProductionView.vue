<template>
  <div class="page">
    <PageHeader>
      {{ $t('production.title') }}
      <template #subtitle>{{ $t('production.eggs') }} · {{ $t('production.flock') }} · {{ $t('production.mortality') }}</template>
    </PageHeader>

    <section v-if="kpis" class="card card-body section-kpis">
      <h2 class="section-title">{{ $t('dashboard.production') }}</h2>
      <div class="kpi-row">
        <span>{{ $t('production.eggs') }}: {{ kpis.eggs_today }} ({{ $t('common.today') }}), {{ kpis.eggs_week }} ({{ $t('common.week') }}), {{ kpis.eggs_month }} ({{ $t('common.month') }})</span>
        <span>Taux casse: {{ kpis.break_rate }}% — {{ $t('production.flock') }}: {{ kpis.current_hens }} — {{ $t('production.mortality') }}: {{ kpis.mortality }}</span>
      </div>
    </section>

    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('production.eggs') }}</h2>
        <button type="button" class="btn btn-primary" @click="eggModalOpen = true">{{ $t('common.add') }}</button>
      </div>
    </section>
    <section class="card card-body">
      <div class="section-header">
        <h2 class="section-title">{{ $t('production.flock') }}</h2>
        <button type="button" class="btn btn-primary" @click="flockModalOpen = true">{{ $t('common.add') }}</button>
      </div>
    </section>

    <Modal v-model="eggModalOpen" :title="$t('common.add') + ' ' + $t('production.eggs')">
      <form @submit.prevent="submitEggs" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="eggForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('production.eggsCount') }}</label>
          <input v-model.number="eggForm.eggs_count" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.brokenCount') }}</label>
          <input v-model.number="eggForm.broken_count" type="number" class="input" min="0" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="eggModalOpen = false">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>

    <Modal v-model="flockModalOpen" :title="$t('common.add') + ' ' + $t('production.flock')">
      <form @submit.prevent="submitFlock" class="form-fields">
        <div class="form-group">
          <label class="required">{{ $t('common.date') }}</label>
          <input v-model="flockForm.date" type="date" class="input" required />
        </div>
        <div class="form-group">
          <label>{{ $t('production.totalHens') }}</label>
          <input v-model.number="flockForm.total_hens" type="number" class="input" min="0" />
        </div>
        <div class="form-group">
          <label>{{ $t('production.dead') }}</label>
          <input v-model.number="flockForm.dead" type="number" class="input" min="0" />
        </div>
        <div class="form-actions">
          <button type="submit" class="btn btn-primary">{{ $t('common.save') }}</button>
          <button type="button" class="btn btn-ghost" @click="flockModalOpen = false">{{ $t('common.cancel') }}</button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Modal from '../components/Modal.vue'
import PageHeader from '../components/PageHeader.vue'
import { createEggs, createFlock, getKpis } from '../api/production'

const kpis = ref(null)
const eggModalOpen = ref(false)
const flockModalOpen = ref(false)
const eggForm = ref({ date: new Date().toISOString().slice(0, 10), eggs_count: 0, broken_count: 0 })
const flockForm = ref({ date: new Date().toISOString().slice(0, 10), total_hens: 0, dead: 0 })

async function loadKpis() {
  try {
    kpis.value = await getKpis()
  } catch (e) {
    console.error(e)
  }
}

async function submitEggs() {
  try {
    await createEggs(eggForm.value)
    eggModalOpen.value = false
    await loadKpis()
  } catch (e) {
    console.error(e)
  }
}

async function submitFlock() {
  try {
    await createFlock(flockForm.value)
    flockModalOpen.value = false
    await loadKpis()
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadKpis)
</script>

<style scoped>
.section-kpis {
  margin-bottom: var(--space-6);
}

.kpi-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

</style>
