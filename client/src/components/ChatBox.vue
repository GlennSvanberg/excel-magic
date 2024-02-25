<template>
    <v-card style="width: 50%; margin: auto;">
        <!-- Messages Display -->
        <v-list two-line style="height: 50vh; overflow: auto;">
            <v-list-item v-for="(msg, index) in messages" :key="index">
                <v-list-item-content>
                    <v-list-item-title>{{ msg.sender }}</v-list-item-title>
                    <v-list-item-subtitle class="wrap-text">{{ msg.message }}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
        </v-list>

        <!-- Input and Send Button -->
        <v-card-actions>
            <v-text-field v-model="inputMessage" placeholder="Type your text here..." @keyup.enter="sendMessage"
                outlined></v-text-field>
            <v-btn color="primary" @click="sendMessage">Send</v-btn>
        </v-card-actions>
    </v-card>
</template>


<script setup lang="ts">
import { ref } from 'vue';
import { useStore } from 'vuex';

const store = useStore();


const messages = ref<{ sender: string; message: string }[]>([]);
const inputMessage = ref('');
const responseFiles = ref<string[]>([]);

const sendMessage = () => {
    if (inputMessage.value) {
        messages.value.push({ sender: 'User', message: inputMessage.value });
        inputMessage.value = '';
        // Here you can send your message to AI Agent
        receiveMessage();
    }
};


async function getMessage() {
    const payload = {
        files: store.state.fileNames,
        messages: messages.value,
    };

    try {
        const response = await fetch('http://localhost:7001/api/do_magic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        const responseData = await response.json();
        console.log(responseData);
        messages.value.push({ sender: 'AI', message: responseData.message });
        const filenames = responseFiles.value.map((file) => file.split('/').pop());
        console.log(filenames);
        responseFiles.value = [];
        filenames.forEach((filename) => {
            if (filename) {
                responseFiles.value.push(filename);
            }
        });
        console.log(responseFiles.value);
    } catch (error) {
        console.error(error);
    }
}

const receiveMessage = () => {
    getMessage();
};

</script>


<style>
.wrap-text {
    white-space: normal;
}
</style>
