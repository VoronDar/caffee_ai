<template>
  <div class="app-container">
  <div class="image-upload-container">
    <ImageUploader />
  </div>
  <div class="report-table-container">
    <ReportTable />
  </div>
  </div>
</template>

<script setup lang="ts">
import ImageUploader from './components/ImageUploader.vue'
import ReportTable from './components/ReportTable.vue'
</script>

<style>
.app-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  width: 100%;
}
.image-upload-container {
  width: 50%;
  float: left;
}
.report-table-container {
  width: 50%;
  float: right;
}
</style>
