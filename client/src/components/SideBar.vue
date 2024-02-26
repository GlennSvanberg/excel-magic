<template>
    <v-list style="display:flex; flex-direction: column;">
        <v-file-input multiple @change="onFilesSelected" @click:clear="clearFiles" label="Select your files"></v-file-input>
        <FileDisplay v-for="filename in fileNames" :key="filename" :fileName="filename" />
        <FileDisplay v-for="filename in outputFilenames" :key="filename" :fileName="filename" />
    </v-list>
</template>

<script setup lang="ts">

import { ref, computed } from 'vue';
import FileDisplay from './FileDisplay.vue';
import { useStore, mapState } from 'vuex';

let fileNames = ref<string[]>([]);

const store = useStore();

const outputFilenames = computed(() => store.state.outputFilenames);

const baseUrl = import.meta.env.VITE_APP_API_BASE_URL as string;
console.log('baseUrl', baseUrl);

async function postFiles(formData: FormData) {
    try {
        const response = await fetch(`${baseUrl}api/upload`, {
            method: 'POST',
            body: formData,
        });
        // Process response if needed
        const responseData = await response.json();
        console.log(responseData);
        console.log('posted file: ', formData.get('file'));
    } catch (error) {
        console.error(error);
    }
}

const onFilesSelected = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const selectedFiles = target?.files;

    if (selectedFiles) {
        const uploadPromises: Promise<void>[] = [];

        Array.from(selectedFiles).forEach((file) => {
            const formData: FormData = new FormData();
            formData.append('file', file, file.name);
            uploadPromises.push(postFiles(formData));
        });

        Promise.all(uploadPromises)
            .then(() => {
                fileNames.value = Array.from(selectedFiles).map((file) => file.name);
                console.log('set filenames:', fileNames.value);
                store.commit('setFileNames', fileNames.value);
            })
            .catch((error) => {
                console.error('Error uploading files:', error);
            });
    }
};

const clearFiles = () => {
    fileNames.value = [];
    store.commit('setFileNames', fileNames.value);
}

</script>
