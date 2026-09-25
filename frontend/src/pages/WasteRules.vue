<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const settings = ref({})
onMounted(async () => { settings.value = await getJSON('/api/settings') })
</script>
<template>
  <div class="page">
    <h1>损耗规则</h1>
    <p>默认损耗率按面积法向上取整后再乘 (1+损耗%)。</p>
    <p>当前默认损耗：<strong>{{ settings.waste_pct }}%</strong></p>
    <p>网格预览块数可能大于面积法片数，下单以面积法 order_count 为准。</p>
    <p>花铺循环：循环长 &gt; 0 时沿房间长边按 ceil(房间长/循环长) 段对接花位，每段重新起砖产生加片，与基础片数合计；循环长 0 为关闭，≥房间长或为负会测算失败。</p>
  </div>
</template>
