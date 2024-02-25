import { createStore } from 'vuex';

interface State {
    fileNames: string[];
    }

    export default createStore({
        state: {
            fileNames: [],
        },
        mutations: {
            setFileNames(state, payload: string[]) {
                state.fileNames = payload;
            },
        }
    });

