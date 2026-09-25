<script setup>
defineProps({
  result: { type: Object, default: null },
})
</script>
<template>
  <div v-if="result" class="order-summary">
    <div class="hero">{{ result.order_count }} 片</div>
    <ul>
      <li>
        基础 {{ result.base_order_count }} 片
        <template v-if="result.pattern_extra > 0">
          ＋ 花铺加片 {{ result.pattern_extra }} 片
          <small>（循环长 {{ result.pattern_cycle }} m，{{ result.pattern.cycles }} 循环 × {{ result.pattern.rows }} 行）</small>
        </template>
        <template v-else><small>（未启用花铺循环）</small></template>
      </li>
      <li>净用量 {{ result.raw_count }} 片，损耗 {{ result.waste_pct }}%</li>
      <li>地面 {{ result.area_m2 }} m²，单砖 {{ result.piece_m2 }} m²</li>
    </ul>
  </div>
</template>
