<template>
  <div class="chatitem">
    <div class="timebox" v-if="message.type == 3">
      {{ message.content }}
    </div>
    <div v-else>
      <div class="usermessagebox" v-if="userIconInfo.myid == message.receiver_id">
        <img :src="userIconInfo.user" alt="" class="usermessageicon">
        <div class="usermessage" v-if="message.type == 1">
          {{ message.content }}
        </div>
        <div class="userimagebox" v-if="message.type == 2">
          <img :src="message.content" alt="" class="userimage">
        </div>
      </div>
      <div class="mymessagebox" v-if="userIconInfo.myid == message.sender_id">
        <div class="mymessage" v-if="message.type == 1">
          {{ message.content }}
        </div>
        <div class="userimagebox" v-if="message.type == 2">
          <img :src="message.content" alt="" class="userimage">
        </div>
        <img :src="userIconInfo.my" alt="" class="mymessageicon">
      </div>
      <div class="othermessagebox" v-if="userIconInfo.myid != message.sender_id && userIconInfo.myid != message.receiver_id">

      </div>
    </div>

  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true
  },
  userIconInfo: {
    type: Object,
    required: true
  }
})
</script>

<style scoped>
.userimage {
  object-fit: cover;
  width: 100%;
}

.userimagebox {
  max-width: 240px;
  overflow: hidden;
  border-radius: 6px;
  border: 1px solid #aaaaaa;
}

.timebox {
  color: #999999;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 20px;
  font-size: 13px;
  margin-top: 16px;
}

.mymessageicon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid #aaaaaa;
  margin-left: 8px;
}

.mymessage {
  background-color: #00AEEC;
  padding: 8px;
  border-radius: 12px 0 12px 12px;
  color: #FFFFFF;
}

.mymessagebox {
  display: flex;
  justify-content: flex-end;
}

.usermessage {
  background-color: #f1f1f1;
  padding: 8px;
  border-radius: 0 12px 12px 12px;
}

.usermessagebox {
  display: flex;
}

.usermessageicon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid #aaaaaa;
  margin-right: 8px;
}

.chatitem {
  padding: 6px 12px;
  font-size: 15px;
}
</style>