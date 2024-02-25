<template>
    <v-card style="width: 50%; margin: auto;">
        <!-- Messages Display -->
        <v-list two-line style="height: 50vh; overflow: auto; ">
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
        // responseDate for testing
        // const responseData: {
        //     files: string[], message: string
        // }
        //     = { files: ["http://localhost:7001/static/output/names.xlsx", "http://localhost:7001/static/output/merged_data.xlsx"], message: "The files have been successfully merged by name, a…ved in a new Excel file named `merged_data.xlsx`." }
        console.log(responseData);
        const responseLinks: string[] = responseData.files;
        store.commit('setOutputLinks', responseLinks);
        const responseMessage: string = responseData.message;
        messages.value.push({ sender: 'AI', message: responseMessage });
        const filenames: (string | undefined)[] = responseData.files.map((file: string) => file.split('/').pop());
        store.commit('clearOutputFilenames');
        filenames.forEach((filename) => {
            if (filename) {
                store.commit('addOutputFilenames', filename);
            }
        });
        console.log(store.state.outputFilenames);
        console.log(store.state.outputLinks);
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
