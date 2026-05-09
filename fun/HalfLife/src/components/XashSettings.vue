<template>
  <div class="xash-settings">
    <div class="xash-menu-flex" v-if="!loading">
      <XashLoadZip />
    </div>
    <XashLoading v-if="loading" />
  </div>
</template>

<script setup lang="ts">
  import { storeToRefs } from 'pinia';
  import { useXashStore } from '/@/stores/store';
  import XashLoading from '/@/components/XashLoading.vue';
  import XashLoadZip from '/@/components/XashLoadZip.vue';

  const store = useXashStore();
  const { loading } = storeToRefs(store);
</script>