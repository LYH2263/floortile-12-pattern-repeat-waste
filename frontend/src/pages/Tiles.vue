<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, patchJSON } from '../api'
const items = ref([])
const savedId = ref(0)
const err = ref('')
onMounted(async () => { items.value = (await getJSON('/api/tiles')).items })
async function saveCycle(t) {
  err.value = ''
  savedId.value = 0
  try {
    const updated = await patchJSON(`/api/tiles/${t.id}`, { pattern_cycle: Number(t.pattern_cycle) || 0 })
    t.pattern_cycle = updated.pattern_cycle
    savedId.value = t.id
  } catch (e) {
    err.value = e.message
  }
}
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <p v-if="err" class="alert">{{ err }}</p>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
        <label>默认花铺循环长(m，0=关闭)
          <input type="number" min="0" step="0.1" v-model.number="t.pattern_cycle" />
        </label>
        <button @click="saveCycle(t)">保存循环长</button>
        <span v-if="savedId === t.id">已保存</span>
      </div>
    </div>
  </div>
</template>
