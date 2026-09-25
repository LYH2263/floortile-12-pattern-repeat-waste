<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>
        基础下单 {{ result.base_order_count }} 片
        <template v-if="result.pattern_cycle > 0">
          ，花铺循环 {{ result.pattern_cycle }} m × {{ result.pattern_cycles }} 段，加片 {{ result.pattern_extra }} 片
        </template>
      </li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>
  </div>
</template>
