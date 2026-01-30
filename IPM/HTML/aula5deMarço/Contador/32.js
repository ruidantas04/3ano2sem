const vueApp = Vue.createApp({
    data () {
        return {
            contador: 0
        }
    },
    methods : {
        incrementa: function(){
            this.contador++
        },
        decrementa: function(){
            this.contador--
        }
    }
})

vueApp.mount('#app')