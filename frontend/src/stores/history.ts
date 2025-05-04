import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export interface HistoryRecord {
  timestamp: string
  people_total: number
  tables_counts: string
}

export const useHistoryStore = defineStore('history', () => {
  const records = ref<HistoryRecord[]>([])

  const fetchHistory = async () => {
    try {
      const response = await axios.get<HistoryRecord[]>('http://localhost:8000/history/')
      records.value = response.data.map(r => ({
        timestamp: new Date(r.timestamp).toLocaleString('ru-RU', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        tables_counts: typeof r.tables_counts === 'string'
          ? Array(JSON.parse(r.tables_counts)).toLocaleString()
          : r.tables_counts,
        people_total: r.people_total,
      }))
    } catch (error) {
      console.error('Не удалось загрузить историю:', error)
    }
  }

  return {
    records,
    fetchHistory
  }
})
