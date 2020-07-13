<template>
  <div id="app">
    <Chat/>
  </div>
</template>

<script>
import Chat from './components/Chat.vue'

export default {
  name: 'App',
  components: {
    Chat
  },
}
</script>

<style lang="scss">
html, body, #app {
  height: 100%;
}
</style>
