import { defineStore } from 'pinia'

export const useToastStore = defineStore({
    id: 'toast',

    state: () => ({
        ms: 0,
        message: '',
        classes: '',
        isVisible: false,
        height: 0,
        width: 0,
        navbarHeight: 0,
        peopleYouMayKnowHeight: 0,
        trendsHeight: 0,
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
        setWidth(data){
            this.width = data
        },
        setNavbarHeight(data){
            this.navbarHeight = data
        },
        setPeopleHeight(data){
            this.peopleYouMayKnowHeight = data
        },
        setTrendsHeight(data){
            this.trendsHeight = data
        },
        resetPeopleHeight(){
            this.peopleYouMayKnowHeight = 0
        },
        resetTrendsHeight(){
            this.peopleYouMayKnowHeight = 0
        }
    }
})