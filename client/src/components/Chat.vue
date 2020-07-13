<template>
  <div class="socket-chat-wrapper">
    <div class="chat-wrapper">
      <div class="message-wrapper" v-for="(message, index) in messages" :key="index">
        <div class="message-sender">
          {{ message.id }}
        </div>
        <div class="message-text">
          {{ message.text }}
        </div>
      </div>
    </div>

    <div class="input-wrapper">
      <b-input type="text" v-model="new_message" class="message-input" placeholder="Введите сообщение">
      </b-input>
      <b-button type="is-primary" @click="sendMessage">
        Отправить
      </b-button>
    </div>
  </div>
</template>

<script>
const io = require('socket.io-client')

export default {
  name: 'Chat',
  data () {
    return {
      socket: null,
      new_message: '',
      messages: [],
      exist_colors: [],
      users: []
    }
  },
  created () {
  //   this.socket = io('localhost:5000')

  //   this.socket.on('chat_message', function (data) {
  //     this.messages.push(data)
  //   }.bind(this))
  // },
  // mounted () {
  //   document.body.addEventListener('keypress', function (event) {
  //     if(event.keyCode === 13 && this.sendMessage) {
  //       this.sendMessage()
  //     }
  //   }.bind(this))
  //   window.addEventListener('beforeunload', function () {
  //     this.socket.close()
  //   }.bind(this))
  // },
  // methods: {
  //   sendMessage () {
  //     this.socket.emit('message', {
  //       id: this.socket.id,
  //       text: this.new_message
  //     })
  //     this.new_message = ''
  //   },
  //   addUser () {

    },
    getRandomColor () {
      return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6)
    }
  }
}
</script>

<style lang="scss">
.socket-chat-wrapper {
  position: relative;

  .chat-wrapper {
    padding: 20px;

    .message-wrapper {
      margin-bottom: 20px;
    }
  }
  .input-wrapper {
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;

    .message-input {
      width: calc(100% - 105px);
    }
  }
}
</style>
