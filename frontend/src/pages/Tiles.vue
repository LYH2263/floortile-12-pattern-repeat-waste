<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, putJSON } from '../api'
const items = ref([])
const drafts = ref({})
const savedId = ref(null)
onMounted(async () => {
  items.value = (await getJSON('/api/tiles')).items
  for (const t of items.value) drafts.value[t.id] = String(t.pattern_cycle ?? 0)
})

async function saveCycle(t) {
  const v = Number(drafts.value[t.id] || 0)
  const updated = await putJSON(`/api/tiles/${t.id}`, { pattern_cycle: v })
  Object.assign(t, updated)
  drafts.value[t.id] = String(updated.pattern_cycle ?? 0)
  savedId.value = t.id
  setTimeout(() => { if (savedId.value === t.id) savedId.value = null }, 2000)
}
</script>
<template>
  <div class="page">
    <h1>砖型库</h1>
    <div class="tile-cards">
      <div v-for="t in items" :key="t.id" class="tile-card" :class="{ dirty: t.data_quality === 'dirty' }">
        <strong>{{ t.name }}</strong>
        <span>{{ t.tile_l }} × {{ t.tile_w }} m</span>
        <em v-if="t.data_quality === 'dirty'">无效规格</em>
        <label v-else>
          默认花铺循环长 (m)
          <input v-model="drafts[t.id]" type="number" min="0" step="0.1" />
        </label>
        <button v-if="t.data_quality !== 'dirty'" @click="saveCycle(t)">存默认</button>
        <small v-if="savedId === t.id" class="saved">已保存</small>
        <small v-else-if="t.data_quality !== 'dirty'">0 = 关闭花铺加片</small>
      </div>
    </div>
  </div>
</template>
