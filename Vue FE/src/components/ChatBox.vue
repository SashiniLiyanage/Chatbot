
<template>
<div class="bg">
<button @click="goToUploadPage">Upload Content</button>
<div class="chatbox-container">
<div class="container">
  <h1>Marshall Chat Bot</h1>
<div class="messageBox mt-8 chat_area"  ref="scrollableDiv">
  <template v-for="(message, index) in messages" :key="index">
    <div :class="message.from == 'user' ? 'messageFromUser' : 'messageFromBot'">
      <div :class="message.from == 'user' ? 'userIcon' : 'botIcon'"></div>
      <div :class="message.from == 'user' ? 'userMessageWrapper' : 'botMessageWrapper'">
        <div :class="message.from == 'user' ? 'userMessageContent' : 'botMessageContent'">{{ message.data }}</div>
      </div>
    </div>
  </template>
  <div v-if="loading">
    <div class="messageFromBot">
      <div class="botIcon"></div>
      <div class="botMessageWrapper">
        <!-- <div class="botMessageContent">Typing...</div> -->
        <div class="botMessageContent">
          <div class="dot-typing"></div>
        </div>
      </div>
    </div>
  </div>

</div>
<div class="inputContainer">
  <input
    v-model="currentMessage"
    type="text"
    class="messageInput"
    placeholder="Ask me anything about Marshall..."
    @keyup.enter="sendMessage(currentMessage)"
  />
  <button
    @click="sendMessage(currentMessage)"
    class="askButton"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
      <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" fill="white"/>
      <path d="M0 0h24v24H0z" fill="none"/>
    </svg>
  </button>
</div>
</div>
</div>
</div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'ChatBox',
  data() {
    return {
      currentMessage: '',
      messages: [],
      loading: false, 
    };
  },
  methods: {
    async sendMessage(message) {
      if(message == "" || this.loading) return;
      
      this.messages.push({
        from: 'user',
        data: message,
      });

      this.loading = true;
      this.currentMessage = '';

      this.scrollToBottomAfterDelay()
      await axios
        .post(process.env.VUE_APP_BE_URL+'/ask', {
          ques: message,
        })
      .then((response) => {
        this.messages.push({
          from: 'bot',
          data: response.data.message,
        });
      }).catch(error => {
          console.error(error);
          this.messages.push({
            from: 'bot',
            data: "Something went wrong! Please try again later.",
        });
      }).finally(()=>{
        this.loading = false;
        this.scrollToBottomAfterDelay()
      });
    },
    scrollToBottom() {
      const scrollableDiv = this.$refs.scrollableDiv;
      scrollableDiv.scrollTop = scrollableDiv.scrollHeight;
    },
    scrollToBottomAfterDelay() {
      setTimeout(() => {
        this.scrollToBottom();
      }, 200);
    },
    goToUploadPage() {
      this.$router.push("/upload");
    },
  },
};
</script>