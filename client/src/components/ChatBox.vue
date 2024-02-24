
<template>
    <v-card style="width: 50%; margin: auto;">
      <!-- Messages Display -->
      <v-list two-line style="height: 50vh; overflow: auto;">
        <v-list-item v-for="(msg, index) in messages" :key="index">
          <v-list-item-content>
            <v-list-item-title>{{ msg.content }}</v-list-item-title>
            <v-list-item-subtitle>{{ msg.source }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <!-- Input and Send Button -->
      <v-card-actions>
        <v-text-field
          v-model="inputMessage"
          placeholder="Type your text here..."
          outlined
        ></v-text-field>
        <v-btn color="primary" @click="sendMessage">Send</v-btn>
      </v-card-actions>
    </v-card>
  </template>


<script setup lang="ts">
import { ref } from 'vue';

const messages = ref<{ source: string; content: string }[]>([]);
const inputMessage = ref('');

const sendMessage = () => {
  if (inputMessage.value) {
    messages.value.push({ source: 'User', content: inputMessage.value });
    inputMessage.value = '';
    // Here you can send your message to AI Agent
  }
};
</script>
