<template>
  <div class="image-uploader">
    <a :href="result.img_url" v-if="result?.img_url" target="_blank" >
      <img :src="result.img_url" class="preview" :alt="`Обнаружено людей: ${result.people_total}, По столам: ${result.tables}`" :title="`Обнаружено людей: ${result.people_total}, По столам: ${result.tables.map(t => t.count).join(', ')}`" />
    </a>
    <div
      class="upload-area"
      @dragover.prevent
      @dragenter.prevent
      @drop.prevent="handleDrop"
    >
      <p v-if="!imagePreview">Перетащите изображение сюда или нажмите для выбора</p>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileChange"
      />
      <img v-if="imagePreview" :src="imagePreview" class="preview" />
      <button @click="triggerFileInput" class="btn">Выбрать файл</button>
    </div>
    <button
      :disabled="!file || loading"
      @click="uploadImage"
      class="btn submit"
    >
      {{ loading ? 'Загрузка...' : 'Отправить' }}
    </button>

    <div v-if="result" class="result">
      <p>Обнаружено людей: {{ result.people_total }}</p>
      <p>По столам: {{ result.tables.map(t => t.count).join(', ') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { useHistoryStore } from '../stores/history'

type Result = {
  timestamp: string
  people_total: number
  tables: { box: Array<string>, count: number }[]
  img_url: string
}

const file = ref<File | null>(null)
const imagePreview = ref<string | null>(null)
const loading = ref(false)
const result = ref<Result | null>()

const historyStore = useHistoryStore()
const fileInput = ref<HTMLInputElement | null>(null)

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    setFile(target.files[0])
  }
}

const handleDrop = (e: DragEvent) => {
  if (e.dataTransfer?.files.length) {
    setFile(e.dataTransfer.files[0])
  }
}

const setFile = (f: File) => {
  file.value = f
  result.value = null
  imagePreview.value = URL.createObjectURL(f)
}

const uploadImage = async () => {
  if (!file.value) return

  loading.value = true
  const formData = new FormData()
  formData.append('file', file.value)

  try {
    const res = await axios.post('http://localhost:8000/count/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    result.value = res.data
    historyStore.fetchHistory()
  } catch (err) {
    console.error('Ошибка при загрузке:', err)
  } finally {
    fileInput.value = null
    imagePreview.value = null
    loading.value = false
    historyStore.fetchHistory()
  }
}
</script>

<style scoped>
.image-uploader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-area {
  border: 2px dashed #ccc;
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  cursor: pointer;
  width: 300px;
  min-height: 200px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.preview {
  max-width: 100%;
  max-height: 180px;
  margin: 0.5rem 0;
}

.hidden {
  display: none;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 5px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.submit {
  background: #28a745;
}

.result {
  margin-top: 1rem;
}
</style>
