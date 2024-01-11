import { defineStore } from 'pinia'

export const useToastStore = defineStore({
    id: 'toast',

    state: () => ({
        ms: 0,
        message: '',
        classes: '',
        isVisible: false,
        height: null,
        navbarHeight: null,
    }),

    actions: {
        showToast(ms, message, classes) {
            this.ms = parseInt(ms)
            this.message = message
            this.classes = classes
            this.isVisible = true

            setTimeout(() => {
                this.classes += ' -translate-y-28 z-50'
            }, 10)

            setTimeout(() => {
                this.classes = this.classes.replace('-translate-y-28 z-50', '')
            }, this.ms - 500)

            setTimeout(() => {
                this.isVisible = false
            }, this.ms)
        },
        setHeight(data){
            this.height = data
        },
        setNavbarHeight(data){
            this.navbarHeight = data
        }
    }
})