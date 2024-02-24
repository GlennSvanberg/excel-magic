<template>
  <v-app>
    <v-layout class="rounded rounded-md">
      <v-app-bar title="Excel AI Helper"></v-app-bar>

      <v-navigation-drawer>
        <SideBar />
      </v-navigation-drawer>

      <v-main class="d-flex flex-column align-center" style="height: 100vh;">
        <ChatBox />
  </v-main>

    </v-layout>
  </v-app>
</template>

<script setup lang="ts">
</script>
