<template>
  <div class="page">
    <PageHeader>
      {{ $t('settings.title') }}
      <template #subtitle>{{ $t('settings.localeLabel') }}</template>
    </PageHeader>

    <section class="card card-body">
      <h2 class="section-title">{{ $t('settings.language') }}</h2>
      <div class="form-fields" style="max-width: 24rem;">
        <div class="form-group">
          <label>{{ $t('settings.localeLabel') }}</label>
          <div class="form-actions">
            <button
              type="button"
              class="btn"
              :class="locale === 'fr' ? 'btn-primary' : 'btn-ghost'"
              @click="setLocale('fr')"
            >
              Français
            </button>
            <button
              type="button"
              class="btn"
              :class="locale === 'en' ? 'btn-primary' : 'btn-ghost'"
              @click="setLocale('en')"
            >
              English
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import PageHeader from '../components/PageHeader.vue'

const { locale } = useI18n()

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('locale', lang)
}
</script>
