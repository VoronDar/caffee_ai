<template>
  <div class="report-table">
    <h2>История проверок</h2>
    <div v-if="records.length" class="report-table-data-container">
    <table border="1" v-if="records.length" class="report-table-data">
      <thead>
        <tr>
          <th>Время</th>
          <th>Людей</th>
          <th>По столам</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(entry, index) in records" :key="index">
          <td>{{ entry.timestamp }}</td>
          <td>{{ entry.people_total }}</td>
          <td>{{ entry.tables_counts }}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <div class="export-buttons" v-if="records.length">
      <a href="http://localhost:8000/export/csv/" target="_blank" download="history.csv">Экспорт в CSV</a>
      <a href="http://localhost:8000/export/excel/" target="_blank" download="history.csv">Экспорт в Excel</a>
    </div>
    <p v-else>История пуста.</p>
  </div>
</template>

<script setup lang="ts">
import { useHistoryStore } from '@/stores/history'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

const {records} = storeToRefs(useHistoryStore())
const {fetchHistory} = useHistoryStore()

onMounted(() => fetchHistory())
</script>

<style scoped>
.report-table {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.report-table-data-container {
  height: 400px;
  overflow: auto;
  display: flex;
}

.report-table-data {
  width: 100%;
}

th {
  position: sticky;
  top: 0;
  background: var(--color-background);
}

.export-buttons {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}
td, th {
  padding: 8px;
}
</style>
