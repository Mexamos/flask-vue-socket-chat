<template>
  <div class="socket-chat-wrapper">
    <div class="chat-wrapper">
      <div class="message-wrapper" v-for="(message, index) in messages" :key="index">
        <div class="message-sender" :style="`color: ${getUserColorBySocketId(message.id)};`">
          {{ getUserLoginBySocketId(message.id) }}:
        </div>
        <div class="message-text">
          {{ message.text }}
        </div>
      </div>
    </div>

    <div class="users-list-wrapper">
      <div class="users-list-title">
        Участники чата:
      </div>

      <div class="users-list-container">
        <div class="user-wrapper" v-for="(user, index) in users" :key="index" :style="`color: ${user.color};`">
          {{ getUserLoginBySocketId(user.id) }}
        </div>
      </div>
    </div>

    <div class="input-wrapper">
      <b-input type="text" v-model="new_message" class="message-input" placeholder="Введите сообщение">
      </b-input>
      <b-button type="is-primary" @click="sendMessage">
        Отправить
      </b-button>
      <b-button type="is-light" @click="user_settings_show = !user_settings_show" class="user-settings-button" title="Пользовательские настройки">
        <img src="../../assets/settings.png">
      </b-button>
    </div>

    <b-sidebar
      type="is-light"
      :fullheight="true"
      :overlay="true"
      :right="true"
      :open.sync="user_settings_show"
    >
      <div class="user-settings-wrapper">
        <div class="user-settings-title">
          Персональные настройки пользователя:
        </div>

        <div class="user-settings-item">
          <b-field label="Логин">
            <b-input v-model="login"></b-input>
          </b-field>
        </div>
      </div>
    </b-sidebar>
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
      users: [],
      user_settings_show: false,
      login: '',
      update_user_timer: null
    }
  },
  created () {
    this.socket = io('localhost:5000')

    this.socket.on('chat_message', function (data) {
      this.messages.push(data)
    }.bind(this))
    this.socket.on('update_user_list', function (users) {
      this.users = users
    }.bind(this))
  },
  mounted () {
    document.body.addEventListener('keypress', function (event) {
      if(event.keyCode === 13 && this.sendMessage) {
        this.sendMessage()
      }
    }.bind(this))
    window.addEventListener('beforeunload', function () {
      this.socket.close()
    }.bind(this))
  },
  watch: {
    login () {
      this.updateUserLogin()
    }
  },
  methods: {
    updateUserLogin () {
      clearTimeout(this.update_user_timer)
      this.update_user_timer = null

      this.update_user_timer = setTimeout(function() {
        let updated_user = JSON.parse(JSON.stringify(this.getUserBySocketId(this.socket.id)))
        updated_user.login = this.login

        this.socket.emit('update_user', updated_user)
      }.bind(this), 1500)
    },
    getUserBySocketId (sid) {
      let index = this.users.findIndex(function(user) {
        if(user.id === sid) return true
        else return false
      })
      if(index !== -1) {
        return this.users[index]
      }
      else {
        return null
      }
    },
    getUserLoginBySocketId (sid) {
      let user = this.getUserBySocketId(sid)
      if(user && user.login && user.login.length > 0) {
        return user.login
      }
      else {
        return sid
      }
    },
    getUserColorBySocketId (sid) {
      let user = this.getUserBySocketId(sid)
      if(user) {
        return user.color
      }
      else {
        return 'black'
      }
    },
    sendMessage () {
      if(this.new_message.length === 0) return
      this.socket.emit('message', {
        id: this.socket.id,
        text: this.new_message
      })
      this.new_message = ''
    },
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

      .message-text {
        word-break: break-all;
      }
    }
  }
  .users-list-wrapper {
    position: absolute;
    right: 20px;
    top: 20px;
    min-width: 250px;
    height: 300px;
    padding: 10px;
    border: 1px solid #7957d5;
    border-radius: 3px;
    opacity: 0.5;
    z-index: 10;
    background: white;

    .users-list-container {

      .user-wrapper {
        margin-bottom: 10px;
      }
    }
  }
  .users-list-wrapper:hover {
    opacity: 1;
  }
  .input-wrapper {
    position: fixed;
    bottom: 0;
    width: 100%;
    display: flex;

    .message-input {
      width: calc(100% - 105px);
    }
    .user-settings-button {
      img {
        width: 20px;
      }
    }
  }
}
.sidebar-content {
  width: auto;

  .user-settings-wrapper {
    height: 100%;
    width: 300px;
    padding: 20px;
  }
}
</style>
