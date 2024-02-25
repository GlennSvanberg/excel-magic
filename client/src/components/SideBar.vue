<template>
    <v-list>
        <v-list-item title="Navigation drawer"></v-list-item>
        <v-file-input multiple @change="onFilesSelected" @click:clear="clearFiles"
            label="Multiple file input"></v-file-input>
        <FileDisplay v-for="filename in fileNames" :key="filename" :fileName="filename" />
    </v-list>
</template>

<script setup lang="ts">

import { ref, onMounted, onUpdated } from 'vue';
import FileDisplay from './FileDisplay.vue';
import { useStore } from 'vuex';

let fileNames = ref<string[]>([]);
let csvData = ref<string[]>([]);


const store = useStore();

async function postFiles(formData: FormData) {
    try {
        const response = await fetch('http://localhost:7001/api/upload', {
            method: 'POST',
            body: formData,
        });
        // Process response if needed
        const responseData = await response.json();
        console.log(responseData);

    } catch (error) {
        console.error(error);
    }
}

async function getFiles(fileNames: string[]): Promise<string[]> {
    const responses: string[] = [];

    for (const fileName of fileNames) {
        try {
            const response = await fetch(`http://localhost:7001/api/uploads/${fileName}`,
                {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                }
            );
            const responseData = await response.json();
            responses.push(responseData);
        } catch (error) {
            console.error(error);
        }
    }
    return responses;
}

const onFilesSelected = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const selectedFiles = target?.files;

    if (selectedFiles) {

        const formData = new FormData();
        Array.from(selectedFiles).forEach(file => {
            formData.append('file', file, file.name);
        });

        postFiles(formData);

        fileNames.value = Array.from(selectedFiles).map(file => file.name);
        store.commit('setFileNames', fileNames.value);
    }
}

const clearFiles = () => {
    fileNames.value = [];
    store.commit('setFileNames', fileNames.value);
}

</script>

