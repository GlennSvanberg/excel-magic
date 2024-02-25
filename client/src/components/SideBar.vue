<template>
    <v-list>
        <v-list-item title="Navigation drawer"></v-list-item>
        <v-file-input multiple @change="onFilesSelected" @click:clear="clearFiles"
            label="Multiple file input"></v-file-input>
        <FileDisplay :files="fileNames" />
    </v-list>
</template>

<script setup lang="ts">
//
import { ref, onMounted, onUpdated } from 'vue';
import FileDisplay from './FileDisplay.vue';
import { useStore } from 'vuex';

let fileNames = ref<string[]>([]);

const store = useStore();

const onFilesSelected = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const selectedFiles = target?.files;

    // Here we call the api endpoint that returns file contents which is passed as state to file display

    if (selectedFiles) {
        for (let i = 0; i < selectedFiles.length; i++) {
            fileNames.value = Array.from(selectedFiles).map(file => file.name);
            console.log("sidebar file chosen:" + fileNames.value);
            store.commit('setFileNames', fileNames.value);
        }
    }
}

const clearFiles = () => {
    fileNames.value = [];
    store.commit('setFileNames', fileNames.value);
}

</script>

