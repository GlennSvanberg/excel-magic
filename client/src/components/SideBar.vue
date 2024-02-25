<template>
    <v-list>
        <v-list-item title="Navigation drawer"></v-list-item>
        <v-file-input multiple @change="onFilesSelected" @click:clear="clearFiles"
            label="Multiple file input"></v-file-input>
        <FileDisplay v-for="filename in fileNames" :key="filename" :fileName="filename" />
    </v-list>
</template>

<script setup lang="ts">

import { ref } from 'vue';
import FileDisplay from './FileDisplay.vue';
import { useStore } from 'vuex';

let fileNames = ref<string[]>([]);


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

const onFilesSelected = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const selectedFiles = target?.files;

    if (selectedFiles) {

        // can only upload 1 file at a time and they need to be sent in seperate formData.
        // should we change in api or live with this here?
        Array.from(selectedFiles).forEach(file => {
            const formData: FormData = new FormData();
            formData.append('file', file, file.name);
            postFiles(formData);
        });

        fileNames.value = Array.from(selectedFiles).map(file => file.name);
        store.commit('setFileNames', fileNames.value);
    }
}

const clearFiles = () => {
    fileNames.value = [];
    store.commit('setFileNames', fileNames.value);
}

</script>

