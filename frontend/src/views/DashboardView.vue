<template>
  <div class="dashboard-page">
    <PageHeader>
      {{ $t('dashboard.title') }}
      <template #subtitle>{{ $t('dashboard.production') }} · {{ $t('dashboard.finance') }} · {{ $t('dashboard.stock') }}</template>
    </PageHeader>

    <div v-if="loading" class="loading-state">
      <div class="loading-spinner" />
      <p>{{ $t('common.loading') }}</p>
    </div>

    <div v-else-if="summary" class="dashboard-grid">
      <section class="section">
        <h2 class="section-title">{{ $t('dashboard.production') }}</h2>
        <div class="kpi-grid">
          <div class="kpi-card">
            <span class="kpi-value">{{ summary.production?.eggs_today ?? 0 }}</span>
            <span class="kpi-label">{{ $t('production.eggs') }} ({{ $t('common.today') }})</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ summary.production?.eggs_week ?? 0 }}</span>
            <span class="kpi-label">{{ $t('common.week') }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ summary.production?.eggs_month ?? 0 }}</span>
            <span class="kpi-label">{{ $t('common.month') }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ summary.production?.current_hens ?? 0 }}</span>
            <span class="kpi-label">{{ $t('production.flock') }}</span>
          </div>
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">{{ $t('dashboard.finance') }}</h2>
        <div class="kpi-grid">
          <div class="kpi-card kpi-card--highlight">
            <span class="kpi-value">{{ formatAmount(summary.finance?.revenue) }}</span>
            <span class="kpi-label">CA</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ formatAmount(summary.finance?.outstanding_sales) }}</span>
            <span class="kpi-label">{{ $t('sales.unpaid') }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ formatAmount(summary.finance?.outstanding_purchases) }}</span>
            <span class="kpi-label">{{ $t('purchases.unpaid') }}</span>
          </div>
          <div class="kpi-card">
            <span class="kpi-value">{{ formatAmount(summary.finance?.result) }}</span>
            <span class="kpi-label">Résultat</span>
          </div>
        </div>
      </section>

      <section class="section">
        <h2 class="section-title">{{ $t('dashboard.stock') }}</h2>
        <div class="kpi-grid">
          <div class="kpi-card">
            <span class="kpi-value">{{ formatAmount(summary.stock?.value) }}</span>
            <span class="kpi-label">Valeur</span>
          </div>
        </div>
      </section>

      <section v-if="chartData.labels?.length" class="section section--chart">
        <h2 class="section-title">{{ $t('production.eggs') }}</h2>
        <div class="card chart-card">
          <div class="chart-container">
            <Line :data="chartData" :options="chartOptions" />
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import PageHeader from '../components/PageHeader.vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'
import { getSummary, getCharts } from '../api/dashboard'
import { useCurrencyFormat } from '../composables/useCurrencyFormat'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

const { t } = useI18n()
const { formatAmount } = useCurrencyFormat()
const loading = ref(true)
const summary = ref(null)
const charts = ref({})

function formatNum(n) {
  if (n == null) return '0'
  return Number(n).toLocaleString()
}

const chartData = computed(() => {
  const egg = charts.value?.egg_production || []
  return {
    labels: egg.map((d) => d.date),
    datasets: [
      {
        label: t('production.eggs'),
        data: egg.map((d) => d.eggs),
        borderColor: 'var(--color-primary)',
        backgroundColor: 'rgba(13, 148, 136, 0.08)',
        fill: true,
        tension: 0.3,
      },
    ],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
  },
  scales: {
    y: { beginAtZero: true },
  },
}

onMounted(async () => {
  try {
    summary.value = await getSummary()
    charts.value = await getCharts()
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  padding: var(--space-10);
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

.section {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.section-title {
  margin: 0;
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-4);
}

.kpi-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  box-shadow: var(--shadow-sm);
  transition: box-shadow var(--transition), border-color var(--transition);
}

.kpi-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-primary-light);
}

.kpi-card--highlight {
  border-left: 4px solid var(--color-primary);
}

.kpi-value {
  display: block;
  font-size: var(--text-xl);
  font-weight: var(--font-bold);
  color: var(--color-text);
  line-height: 1.2;
}

.kpi-label {
  display: block;
  margin-top: var(--space-1);
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}

.section--chart .section-title {
  margin-bottom: var(--space-2);
}

.chart-card {
  padding: var(--space-6);
}

.chart-container {
  height: 280px;
}
</style>
