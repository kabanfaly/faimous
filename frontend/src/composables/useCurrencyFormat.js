import { computed } from 'vue'
import { useAuthStore } from '../store/auth'
import { useI18n } from 'vue-i18n'

/**
 * Format amounts using the organisation's default currency and app locale.
 * @returns {{ formatAmount: (value: number | string | null | undefined) => string }}
 */
export function useCurrencyFormat() {
  const auth = useAuthStore()
  const { locale } = useI18n()

  const formatter = computed(() => {
    const currency = auth.organisation?.currency_default || 'GNF'
    const localeStr = locale.value === 'fr' ? 'fr-FR' : 'en-US'
    return new Intl.NumberFormat(localeStr, {
      style: 'currency',
      currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  })

  function formatAmount(value) {
    if (value == null || value === '') return '—'
    const num = Number(value)
    if (Number.isNaN(num)) return '—'
    return formatter.value.format(num)
  }

  return { formatAmount }
}
