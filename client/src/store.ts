import { createStore } from 'vuex';

interface State {
    fileNames: string[];
    outputLinks: string[];
    outputFilenames: string[];
    }

    export default createStore({
        state: (): State => ({
            fileNames: [],
            outputLinks: [],
            outputFilenames: [],
        }),
        mutations: {
            setFileNames(state, payload: string[]) {
                state.fileNames = payload;
            },
            addFileNames(state, payload: string) {
                state.fileNames.push(payload);
            },
            setOutputLinks(state, payload: string[]) {
                state.outputLinks = payload;
            },
            setOutputFilenames(state, payload: string[]) {
                state.outputFilenames = payload;
            },
            addOutputFilenames(state, payload: string) {
                state.outputFilenames.push(payload);
            },
            clearOutputFilenames(state) {
                state.outputFilenames = [];
            }
        }
    });

