<template>
    <v-card class="rounded rounded-md" style="margin-top: 2vh" width="100%" color="primary">
        <v-card-title>
            <h2 class="text-center">{{ fileName }}</h2>
        </v-card-title>
        <v-data-table-virtual :items="tableData"></v-data-table-virtual>
    </v-card>
</template>

<script lang="ts">
import { PropType, defineComponent, ref, watch } from 'vue';
import Papa from 'papaparse';

const baseUrl = import.meta.env.VITE_APP_API_BASE_URL as string;
console.log('baseUrl', baseUrl);
console.log(import.meta.env);

export default defineComponent({
    props: {
        fileName: {
            type: String as PropType<string>,
            required: true,
        },
    },
    setup(props) {
        const fileContent = ref('');
        const tableHeader = ref();
        const tableData = ref();

        // Watch for changes in the fileName prop
        watch(() => props.fileName, (newFileName, oldFileName) => {
            fetchData(newFileName);
        });

        async function fetchData(fileName: string) {
            // Perform data fetching based on the fileName
            // Example code:
            try {
                const response = await fetch(`${baseUrl}api/uploads/${fileName}`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                );
                const responseData = await response.json();
                Papa.parse(responseData, {
                    header: true,
                    complete: (result) => {
                        if (result.meta.fields) {
                            tableHeader.value = result.meta.fields;
                        }
                        if (result.data) {
                            tableData.value = result.data as any;
                        }
                    },
                });
                fileContent.value = responseData;
            } catch (error) {
                console.error(error);
            }
        }

        // Initial data fetch
        fetchData(props.fileName); // Fetch data when the component is mounted or when the prop changes initially

        return {
            fileContent,
            tableHeader,
            tableData,
        };
    },
});



async function getFiles(fileNames: string[]): Promise<string[]> {
    const responses: string[] = [];

    for (const fileName of fileNames) {
    }
    return responses;
}

</script>

