<template>
  <v-list>
    <v-list-item v-for="(file, index) in files" :key="index">
      {{ file }}
    </v-list-item>
  </v-list>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';

export default defineComponent({
  props: {
    files: {
      type: Array as PropType<string[]>,
      required: true
    }
  }
});
</script>

