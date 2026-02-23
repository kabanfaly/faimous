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
        <span>{{ $t('production.breakRate') }}: {{ kpis.break_rate }}% — {{ $t('production.flock') }}: {{ kpis.current_hens }} — {{ $t('production.mortality') }}: {{ kpis.mortality }}</span>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PageHeader from '../components/PageHeader.vue'
import { getKpis } from '../api/production'

const kpis = ref(null)

async function loadKpis() {
  try {
    kpis.value = await getKpis()
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
