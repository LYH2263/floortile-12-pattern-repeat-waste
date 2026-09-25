<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
const openId = ref(null)
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })

function toggle(id) {
  openId.value = openId.value === id ? null : id
}
</script>
<template>
  <div class="page">
    <h1>测算记录</h1>
    <table class="tbl">
      <thead><tr><th>时间</th><th>房间</th><th>砖型</th><th>基础片数</th><th>花铺加片</th><th>合计片数</th><th></th></tr></thead>
      <tbody>
        <template v-for="r in items" :key="r.id">
          <tr>
            <td>{{ r.created_at?.slice(0, 19) }}</td>
            <td>{{ r.room_name }}</td>
            <td>{{ r.tile_name }}</td>
            <td>{{ r.result?.base_order_count ?? r.result?.order_count }}</td>
            <td>{{ r.result?.pattern_extra ?? 0 }}</td>
            <td>{{ r.result?.order_count }}</td>
            <td><button @click="toggle(r.id)">{{ openId === r.id ? '收起' : '详情' }}</button></td>
          </tr>
          <tr v-if="openId === r.id" class="detail-row">
            <td colspan="7">
              <ul>
                <li>花铺循环长：{{ r.result?.pattern_cycle ? r.result.pattern_cycle + ' m' : '未启用（0）' }}</li>
                <li v-if="r.result?.pattern_extra">
                  加片明细：{{ r.result.pattern.cycles }} 循环 × {{ r.result.pattern.rows }} 行 = {{ r.result.pattern_extra }} 片
                </li>
                <li>净用量 {{ r.result?.raw_count }} 片，损耗 {{ r.result?.waste_pct }}%</li>
                <li>备注：{{ r.note || '—' }}</li>
              </ul>
            </td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>
