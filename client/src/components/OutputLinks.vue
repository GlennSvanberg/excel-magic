<template>
    <div>
        <v-card @click="downloadFile" class="file-card">
            <v-card-text class="text-center">
                <v-icon large>mdi-file-download</v-icon>
                <div class="file-name">{{ getFilenameFromUrl(file) }}</div>
            </v-card-text>
        </v-card>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    props: {
        file: {
            type: String, // Assuming the file prop is a string containing the file link
            required: true,
        },
    },
    methods: {
        getFilenameFromUrl(url: string): string {
            const fileName = url.split('/').pop();
            return fileName ? fileName : '';
        },
        downloadFile(): void {
            const link = document.createElement('a');
            link.href = this.file;
            link.download = this.getFilenameFromUrl(this.file);
            link.target = '_blank';
            link.click();
        },
    },
});
</script>

<style scoped>
.file-card {
    cursor: pointer;
    max-width: 200px;
    margin: 0 auto;
    padding: 10px;
}

.file-name {
    font-size: 14px;
    margin-top: 10px;
}
</style>

