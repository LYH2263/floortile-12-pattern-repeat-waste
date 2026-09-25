<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const props = defineProps({ id: String })
const run = ref(null)
const err = ref('')
onMounted(async () => {
  try {
    run.value = await getJSON(`/api/runs/${props.id}`)
  } catch (e) {
    err.value = e.message
  }
})
</script>
<template>
  <div class="page" v-if="run">
    <h1>测算详情 #{{ run.id }}</h1>
    <dl>
      <dt>时间</dt><dd>{{ run.created_at?.slice(0, 19) }}</dd>
      <dt>房间</dt><dd>{{ run.room_name }}</dd>
      <dt>砖型</dt><dd>{{ run.tile_name }}</dd>
      <dt>损耗</dt><dd>{{ run.waste_pct }}%</dd>
      <dt>净用量</dt><dd>{{ run.result?.raw_count }} 片</dd>
      <dt>基础下单</dt><dd>{{ run.result?.base_order_count ?? run.result?.order_count }} 片</dd>
      <dt>花铺循环长</dt><dd>{{ run.result?.pattern_cycle ?? 0 }} m<template v-if="run.result?.pattern_cycles">（{{ run.result.pattern_cycles }} 段）</template></dd>
      <dt>循环加片</dt><dd>{{ run.result?.pattern_extra ?? 0 }} 片</dd>
      <dt>合计下单</dt><dd><strong>{{ run.result?.order_count }} 片</strong></dd>
      <dt>备注</dt><dd>{{ run.note || '—' }}</dd>
    </dl>
    <router-link to="/history">返回记录</router-link>
  </div>
  <div class="page" v-else>
    <h1>测算详情</h1>
    <p v-if="err" class="alert">{{ err }}</p>
  </div>
</template>
